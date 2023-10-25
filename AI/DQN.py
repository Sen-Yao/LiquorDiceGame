import random
import torch
import time
from torch import nn

from GameAI import AI


def try_gpu(i=0):  #@save
    """如果存在，则返回gpu(i)，否则返回cpu()"""
    if torch.cuda.device_count() >= i + 1:
        return torch.device(f'cuda:{i}')
    return torch.device('cpu')


class DQN_agent(AI):
    def __init__(self, num_player, need_output=False):
        super().__init__(num_player, need_output)
        self.trainer = None
        self.length_of_guess_vector = 61
        self.net = nn.Sequential(nn.Linear(10, 256),
                                 nn.ReLU(),
                                 nn.Linear(256, 1024),
                                 nn.ReLU(),
                                 nn.Linear(1024, 4096),
                                 nn.ReLU(),
                                 nn.Linear(4096, 1024),
                                 nn.ReLU(),
                                 nn.Linear(1024, 256),
                                 nn.ReLU(),
                                 nn.Linear(256, 61))
        self.net.to(try_gpu())
        self.loss_function = nn.MSELoss()
        self.epoch = 0
        self.last_epoch = self.epoch
        self.reward_vector = torch.zeros((61,), device=try_gpu())
        self.learning_rate = 0.01
        self.name = 'DQN'
        self.guess = [-1, -1, False, self.name]
        self.need_stuck = False
        self.avg_loss = 0
        self.decide_loss = 0
        self.decide_try = 0
        self.update_time = 0
        self.trainer = torch.optim.Adam(self.net.parameters(), lr=self.learning_rate)

    def InitNet(self):
        # Initial net
        def init_weights(m):
            if type(m) == nn.Linear:
                nn.init.normal_(m.weight, std=0.01)

        self.net.apply(init_weights)

    def Update(self, input_last_guess):
        # Set args
        self.update_time += 1
        input_last_guess.append(self.num_player)
        input_last_guess = torch.tensor(input_last_guess, dtype=torch.float,  device=try_gpu())
        expect_vector = self.net(input_last_guess)
        loss = self.loss_function(expect_vector, self.reward_vector)
        self.avg_loss += loss
        self.trainer.zero_grad()
        loss.backward()
        self.trainer.step()
        if self.epoch % 1000 == 9:
            self.avg_loss = self.avg_loss / (self.update_time * self.length_of_guess_vector)
            # self.decide_loss = self.decide_loss / self.decide_try
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                  f'epoch {self.epoch}，loss:', float(self.avg_loss),
                  '，平均误差为', self.decide_loss)
            self.last_epoch = self.epoch
            self.decide_loss = 0.0
            self.avg_loss = 0
            self.decide_try = 0
            self.update_time = 0

    def Decide(self, last_guess, greedy_epsilon):
        self.decide_try += 1
        self.guess = [-1, -1, False, self.name]
        # Initial input vector
        epsilon = random.random()
        # is greedy
        if epsilon < greedy_epsilon:
            return self.GreedyDecide(last_guess)
        else:
            state_vector = [last_guess[0], last_guess[1], int(last_guess[2]), 0, 0, 0, 0, 0, 0]
            for i in range(6):
                state_vector[3 + i] = self.dice_dict[i]
            state_vector.append(self.num_player)
            state_vector = torch.tensor(state_vector, dtype=torch.float,  device=try_gpu())
            guess_vector = self.net(state_vector)
            max_index = int(torch.argmax(guess_vector))
            if max_index == 60:
                self.guess = [0, 0, False]
            elif last_guess[0] == -1:
                self.guess[0] = int(max_index // 12) + self.num_player
            # last is fei, and now self decide to zhai or 1
            elif (not last_guess[2] and last_guess[1] != 1) and (max_index % 2 == 1 or (max_index % 12 // 2) + 1 == 1):
                self.guess[0] = int(max_index // 12) + last_guess[0] // 2
            # last is zhai or 1, and now self decide to fei
            elif (last_guess[2] or last_guess[1] == 1) and (max_index % 2 == 0 and (max_index % 12 // 2) + 1 != 1):
                self.guess[0] = int(max_index // 12) + last_guess[0] * 2
            else:
                self.guess[0] = int(max_index // 12) + last_guess[0]
            self.guess[2] = bool(max_index % 2)
            self.guess[1] = int(max_index % 12 // 2) + 1
            # print(guess_vector, '\n',  self.reward_vector)
            # print('依据 DQN 计算出的 Q 值，', float(guess_vector[max_index]))
            # print('但实际上此处的 reward', int(self.reward_vector[max_index]))
            self.decide_loss += abs(float(guess_vector[max_index])-int(self.reward_vector[max_index]))
            if self.need_output:
                print('Decide 函数发现 max_index 为', max_index)
                print('依据 DQN 计算出的 Q 值，', float(guess_vector[max_index]))
                print('但实际上此处的 reward', int(self.reward_vector[max_index]))
                if self.guess[0] == 0:
                    print(self.guess[0], self.guess[1], self.guess[2])
                    print(self.name, '玩家选择开！')
                elif self.guess[2]:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    print(self.guess)
                else:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                    print(self.guess)
            return self.guess

    def GetReward(self, last_guess, this_guess, reward, lr):
        if last_guess[0] == -1:
            if this_guess[0] == 0:
                max_index = 60
            else:
                max_index = 12 * (this_guess[0] - self.num_player)
                max_index = 2 * (this_guess[1] - 1) + max_index
                max_index = int(this_guess[2]) + max_index
        elif last_guess[0]+5 == this_guess[0]:
            max_index = 60
        # last is fei, and now self decide to zhai or 1
        elif (not last_guess[2] and last_guess[1] != 1) and (this_guess[1] == 1 or this_guess[2]):
            max_index = 12 * (this_guess[0] - last_guess[0] // 2)
            max_index = 2 * (this_guess[1] - 1) + max_index
            max_index = int(this_guess[2]) + max_index
        # last is zhai or 1, and now self decide to fei
        elif (last_guess[2] or last_guess[1] == 1) and (this_guess[1] != 1 and not this_guess[2]):
            max_index = 12 * (this_guess[0] - last_guess[0] * 2)
            max_index = 2 * (this_guess[1] - 1) + max_index
            max_index = int(this_guess[2]) + max_index
        else:
            max_index = 12 * (this_guess[0] - last_guess[0])
            max_index = 2 * (this_guess[1] - 1) + max_index
            max_index = int(this_guess[2]) + max_index
        self.reward_vector[max_index] = reward
        if self.need_output:
            print(last_guess, '下的决定', this_guess, '在 GetReward 函数中产生了对应的 max_index =', max_index, '产生了',  reward, '的反馈')
        self.learning_rate = lr

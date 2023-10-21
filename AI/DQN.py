import torch
from torch import nn

from GameAI import AI


class DQN_agent(AI):
    def __init__(self, num_player, need_output=False):
        super().__init__(num_player, need_output)
        self.length_of_guess_vector = num_player * 60 + 1
        self.net = nn.Sequential(nn.Linear(9, 256),
                                 nn.ReLU(),
                                 nn.Linear(256, self.length_of_guess_vector))
        self.loss_function = nn.MSELoss()
        self.trainer = torch.optim.SGD(self.net.parameters(), lr=0.1)
        self.epoch = 0
        self.reward_vector = torch.zeros((self.length_of_guess_vector, ))
        self.learning_rate = 0.1
        self.name = 'DQN'
        self.need_stuck = True

    def InitNet(self):
        # Initial net
        def init_weights(m):
            if type(m) == nn.Linear:
                nn.init.normal_(m.weight, std=0.01)

        self.net.apply(init_weights)

    def Update(self, input_last_guess):
        # Set args
        self.trainer = torch.optim.SGD(self.net.parameters(), lr=self.learning_rate)

        loss = self.loss_function(self.net(input_last_guess), self.reward_vector)
        self.trainer.zero_grad()
        loss.backward()
        self.trainer.step()
        print(f'epoch {self.epoch + 1}, loss {loss:f}')

    def Decide(self, last_guess, ge):
        # Initial input vector
        while self.need_stuck:
            for index in range(self.length_of_guess_vector):
                self.guess[2] = bool(index % 2)
                self.guess[1] = int(index % 12 // 2) + 1
                self.guess[0] = int(index // 12) + 1
                if self.need_output:
                    if self.guess[0] == 11:
                        self.guess[0] = 0
                        self.guess[1] = 0
                        self.guess[2] = False
                        print(0, 0, False)
                        print(self.name, '玩家选择开！')
                    elif self.guess[2]:
                        print(self.name, '玩家家喊出', self.guess[0], '个', self.guess[1], '斋')
                        print(self.guess)
                    else:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                        print(self.guess)
                yield self.guess
            print('已遍历所有可能！')
            state_vector = [last_guess[0], last_guess[1], int(last_guess[2]), 0, 0, 0, 0, 0, 0]
            for i in range(6):
                state_vector[3 + i] = self.dice_dict[i]
            state_vector = torch.tensor(state_vector, dtype=torch.float)
            self.Update(state_vector)
            self.need_stuck = False
            break
        while not self.need_stuck:
            state_vector = [last_guess[0], last_guess[1], int(last_guess[2]), 0, 0, 0, 0, 0, 0]
            for i in range(6):
                state_vector[3+i] = self.dice_dict[i]
            state_vector = torch.tensor(state_vector, dtype=torch.float)
            guess_vector = self.net(state_vector)
            max_index = torch.argmax(guess_vector)
            if max_index == 120:
                self.guess = [0, 0, 'False']
            else:
                self.guess[2] = bool(max_index % 2)
                self.guess[1] = int(max_index % 12 // 2) + 1
                self.guess[0] = int(max_index // 12) + 1
            if self.need_output:
                if self.guess[0] == 0:
                    print(self.guess[0], self.guess[1], self.guess[2])
                    print(self.name, '玩家选择开！')
                if self.guess[2]:
                    print(self.name, '玩家家喊出', self.guess[0], '个', self.guess[1], '斋')
                    print(self.guess)
                else:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                    print(self.guess)
            self.need_stuck = True
            yield self.guess

    def GetReward(self, last_guess, this_guess, reward, lr, is_game):
        max_index = 12 * (this_guess[0] - 1)
        max_index = 2 * (this_guess[1] - 1) + max_index
        max_index = int(this_guess[2]) + max_index

        self.learning_rate = lr
        self.reward_vector[max_index] = reward


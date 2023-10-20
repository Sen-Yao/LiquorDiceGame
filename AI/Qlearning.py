import torch
import torch.quantization as quantization
import random
from GameAI import AI

NumPlayer = 2
Learning_rate = 0.1
Discount_factor = 0.1
Epoch = 100000000


class QlearningAIOneLevel(AI):
    """
    An AI based on Q-learning algorithm to generate a response. It is a one level Q-learning, means that it will only
    consider the last input_guess to generate his response
    """

    def __init__(self, num_player, need_output=False):
        """
        Initialize the base information
        """
        super().__init__(num_player, need_output)
        self.num_state = 12210 * self.num_player
        self.num_action = 55 * self.num_player + 1
        self.Q_table = torch.zeros((5 * self.num_player + 2, 6, 2, 6, 6, 6, 6, 6, 5 * self.num_player + 1, 7, 2),
                                   dtype=torch.int8)
        self.trainable = True
        self.name = 'Q'

    def update_Q(self, last_guess, this_guess, reward, lr, is_game):
        # print(last_guess, this_guess)
        Q_value = float(self.Q_table[last_guess[0] + 1][last_guess[1] - 1][int(last_guess[2])][
                            self.dice[0] - 1][self.dice[1] - 1][self.dice[2] - 1][self.dice[3] - 1][self.dice[4] - 1][
                            this_guess[0]][this_guess[1]][int(this_guess[2])])
        Q_value = (1 - lr) * Q_value + lr * reward
        if self.need_output or is_game:
            print(self.name, '更新前 Q 值 为', float(self.Q_table[last_guess[0] + 1][last_guess[1] - 1][int(last_guess[2])][
                                              self.dice[0] - 1][self.dice[1] - 1][self.dice[2] - 1][self.dice[3] - 1][
                                              self.dice[4] - 1][
                                              this_guess[0]][this_guess[1]][int(this_guess[2])]),
                  'reward=', reward, '更新后 Q_value=', Q_value)
        self.Q_table[last_guess[0] + 1][last_guess[1] - 1][int(last_guess[2])][
            self.dice[0] - 1][self.dice[1] - 1][self.dice[2] - 1][self.dice[3] - 1][self.dice[4] - 1][
            this_guess[0]][this_guess[1]][int(this_guess[2])] = Q_value

    def Decide(self, last_guess, greedy_epsilon):
        """
        The AI will react depends on its dices result only
        :return: An action list
        """
        self.guess = [0, 0, False]
        epsilon = random.random()
        # is greedy
        if epsilon < greedy_epsilon:
            if self.need_output:
                print('贪婪！')
            self.guess = [random.randint(0, 5 * self.num_player), random.randint(0, 6), bool(random.randint(0, 1))]
            if self.guess[0] == 0:
                if self.need_output:
                    print(self.name, '玩家玩家选择开！')
                return self.guess
            if self.guess[2]:
                if self.need_output:
                    print(self.name, '玩家玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                return self.guess
            else:
                if self.need_output:
                    print(self.name, '玩家玩家喊出', self.guess[0], '个', self.guess[1])
                return self.guess
        else:
            new_Q_table = self.Q_table[last_guess[0] + 1][last_guess[1] - 1][int(last_guess[2])][
                self.dice[0] - 1][self.dice[1] - 1][self.dice[2] - 1][self.dice[3] - 1][self.dice[4] - 1]
            # Find the biggest Q in new_Q_table
            max_value = torch.max(new_Q_table)
            float_tensor = new_Q_table.dequantize()
            max_index = torch.argmax(float_tensor)
            self.guess[2] = bool(max_index % 2)
            self.guess[1] = int(max_index % 14 // 2)
            self.guess[0] = int(max_index // 14)
            if self.need_output:
                print('依据位于', self.guess, '依据 Q 值为', float(max_value))
            if self.guess[0] == 0:
                if self.need_output:
                    print(self.guess[0], self.guess[1], self.guess[2])
                    print(self.name, '玩家选择开！')
                return self.guess
            if self.guess[2]:
                if self.need_output:
                    print(self.name, '玩家家喊出', self.guess[0], '个', self.guess[1], '斋')
                    print(self.guess)
                return self.guess
            else:
                if self.need_output:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                    print(self.guess)
                return self.guess

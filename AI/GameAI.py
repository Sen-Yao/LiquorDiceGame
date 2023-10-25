import torch
import random


class AI:
    def __init__(self, num_player, need_output, allow_stuck=True):
        """
        Initialize the base information

        """
        self.avg_loss = None
        self.net = None
        self.epoch = None
        self.name = 'AI'
        self.num_player = num_player
        self.dice = torch.randint(1, 7, (5,))
        self.dice = self.dice.sort()[0]
        unique_values = torch.unique(self.dice)
        # shake again
        while len(unique_values) == 5:
            self.dice = torch.randint(1, 7, (5,))
            unique_values = torch.unique(self.dice)
        self.second_dice = self.dice
        self.player_id = None
        self.guess = [-1, -1, False, self.name]
        self.dice_dict = [0, 0, 0, 0, 0, 0]
        self.need_output = need_output
        self.trainable = False
        self.need_stuck = False
        self.allow_stuck = allow_stuck

    def ShakeDice(self):
        self.dice_dict = [0, 0, 0, 0, 0, 0]
        self.dice = torch.randint(1, 7, (5,))
        self.dice = self.dice.sort()[0]
        unique_values = torch.unique(self.dice)
        # shake again
        while len(unique_values) == 5:
            self.dice = torch.randint(1, 7, (5,))
            unique_values = torch.unique(self.dice)
        self.second_dice = self.dice
        for i in self.dice:
            for j in range(6):
                if i == j + 1:
                    self.dice_dict[j] = self.dice_dict[j] + 1

    def ShowDice(self):
        if self.need_output:
            print(self.name, '玩家的骰子结果为', self.dice)

    def Decide(self, player_number, need_debug_info):
        pass

    def GetReward(self, last_guess, this_guess, reward, lr):
        pass

    def GreedyDecide(self, last_guess):
        if self.need_output:
            print('贪婪！')
        if last_guess[0] == -1:
            self.guess = [random.randint(0, 6) + self.num_player, random.randint(1, 6), bool(random.randint(0, 1))]
        else:
            epsilon2 = random.random()
            if epsilon2 < 0.5:
                if self.need_output:
                    print(self.name, '玩家选择开！')
                self.guess = [0, 0, False]
                return self.guess
            else:
                self.guess = [random.randint(1, 6) + last_guess[0], random.randint(1, 6), bool(random.randint(0, 1))]
                if self.guess[2]:
                    if self.need_output:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                else:
                    if self.need_output:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                    return self.guess

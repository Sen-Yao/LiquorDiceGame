import torch
import random


class AI:
    def __init__(self, num_player, need_output):
        """
        Initialize the base information

        """

        self.dice = None
        self.dice_dict = None
        self.ShakeDice()
        self.name = 'AI'
        self.num_player = num_player
        self.player_id = None
        self.guess = [-1, -1, False, self.name]
        self.need_output = need_output
        self.trainable = False

        # For DQN AI
        self.net = None
        self.decide_try = None
        self.decide_loss = None
        self.update_time = None
        self.avg_loss = None

    def ShakeDice(self):
        self.dice_dict = [0, 0, 0, 0, 0, 0]
        self.dice = torch.randint(1, 7, (5,))
        self.dice = self.dice.sort()[0]
        unique_values = torch.unique(self.dice)
        # If Shunzi, Shake again
        while len(unique_values) == 5:
            self.dice = torch.randint(1, 7, (5,))
            self.dice = self.dice.sort()[0]
            unique_values = torch.unique(self.dice)
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
            self.guess = [random.randint(0, 4) + self.num_player, random.randint(1, 6), bool(random.randint(0, 1))]
            if self.need_output:
                if self.guess[2]:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                else:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
            return self.guess
        else:
            epsilon2 = random.random()
            epsilon3 = random.random()
            if epsilon2 < 0.5:
                if self.need_output:
                    print(self.name, '玩家选择开！')
                self.guess = [0, 0, False]
                return self.guess
            elif 0.5 <= epsilon2 < 0.75:
                if last_guess[2] or last_guess[1] == 1:
                    if epsilon3 < 0.75:
                        self.guess = [random.randint(0, 4) + last_guess[0], random.randint(2, 6), True]
                    else:
                        self.guess = [random.randint(0, 4) + last_guess[0], 1, False]
                else:
                    if epsilon3 < 0.75:
                        self.guess = [random.randint(0, 4) + last_guess[0] // 2, random.randint(2, 6), True]
                    else:
                        self.guess = [random.randint(0, 4) + last_guess[0] // 2, 1, False]
                if self.need_output:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                return self.guess
            else:
                if last_guess[2] or last_guess[1] == 1:
                    self.guess = [random.randint(0, 4) + 2 * last_guess[0], random.randint(2, 6), False]
                else:
                    self.guess = [random.randint(0, 4) + last_guess[0], random.randint(2, 6), False]
                if self.need_output:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                return self.guess

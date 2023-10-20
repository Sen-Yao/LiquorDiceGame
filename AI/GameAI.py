import torch


class AI:
    def __init__(self, num_player, need_output):
        """
        Initialize the base information

        """
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

    def rename(self, name):
        self.name = name

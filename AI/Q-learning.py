import torch

NumPlayer = 2


class AI:
    def __init__(self):
        """
        Initialize the base information

        """
        self.num_player = NumPlayer
        self.dice = torch.randint(1, 7, (5,))
        self.player_id = None
        self.guess = [-1, -1, False]
        self.dice_dict = [0, 0, 0, 0, 0, 0]

    pass


DEFAULT_GAME_CONFIG = {
    'game_num_players': 2
}


class DumpAI(AI):
    """
    A dump AI, base on traditional algorithm to generate a response.
    """

    def __init__(self):
        """
        Initialize the base information
        """
        super().__init__()

    def ShowDice(self):
        print(self.player_id, '号玩家的骰子结果为', self.dice)

    def Decide(self, input_list):
        """
        The AI will react depends on its dices result only
        :return: An action list
        TODO: 搞清楚most_frequent_value_num到底是啥
        """
        # Create a list to store the number of each number
        self.dice_dict = [0, 0, 0, 0, 0, 0]
        for i in self.dice:
            for j in range(6):
                if i == j + 1:
                    self.dice_dict[j] = self.dice_dict[j] + 1
        unique_values, counts = torch.unique(self.dice, return_counts=True)
        most_frequent_value_num = int(unique_values[counts.argmax()]) + self.dice_dict[0]
        real_most_frequent_value_num = int(unique_values[counts.argmax()])

        last_player_num = input_list[0]
        last_player_face = input_list[1]

        # For the face guessed by the last player, the number of dice that AI have
        # Zhai or 1
        if last_player_face == 1 or input_list[2]:
            respond_num = self.dice_dict[last_player_face - 1]
        else:
            respond_num = self.dice_dict[last_player_face - 1] + self.dice_dict[0]
        print('debug:respond_num=', respond_num)
        print('debug:most_frequent_value_num=', most_frequent_value_num)

        # This AI is the beginner
        if input_list[0] == -1:
            if most_frequent_value_num == 1:
                self.guess = [NumPlayer, 1, False]
            else:
                self.guess = [int(NumPlayer + 1), int(unique_values[counts.argmax()]), False]
            print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1])
            return self.guess
        # This AI is responding
        else:
            # Zhai or 1
            if (input_list[1] == 1) or input_list[2]:
                # This AI think he has enough same dice and won't be too dangerous to be opened
                if last_player_num - respond_num < (5 * (self.num_player - 1) / 6):
                    self.guess = [int(input_list[0] + 1), int(input_list[1]), True]
                    print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # Try Fei
                if self.dice_dict[input_list[1] - 1] < self.dice_dict[0]:
                    self.guess = [2 * input_list[0], int(input_list[1]), False]
                    print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1], '飞')
                    return self.guess
                # Try change
                if self.dice_dict[real_most_frequent_value_num - 1] + 5 * (self.num_player - 1) / 3 > input_list[0] - 1\
                        and real_most_frequent_value_num != 1:
                    self.guess = [int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 3),
                                  self.dice_dict[real_most_frequent_value_num-1], True]
                    print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # Try change and Fei
                if self.dice_dict[most_frequent_value_num - 1] + 5 * (self.num_player - 1) / 6 > input_list[0] - 1:
                    self.guess = [int(most_frequent_value_num + 5 * (self.num_player - 1) / 6),
                                  self.dice_dict[most_frequent_value_num-1], False]
                    print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1], '飞')
                    return self.guess
                # This AI think last guess is too big
                else:
                    print(self.player_id, '号玩家选择主动开！')
                    return [0, 0, False]  # Open
            # Normal
            else:
                # This AI think he has enough same dice and won't be too dangerous to be opened
                if last_player_num - respond_num < (5 * (self.num_player - 1) / 3):
                    self.guess = [int(input_list[0] + 1), int(input_list[1]), False]
                    print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1])
                    return self.guess
                # Try Zhai
                if self.dice_dict[input_list[1]-1] > self.dice_dict[0]:
                    self.guess = [int((input_list[0]) / 2 + 1), int(input_list[1]), True]
                    print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # Try change
                if self.dice_dict[most_frequent_value_num - 1] + 5 * (self.num_player - 1) / 3 > input_list[0] - 1:
                    self.guess = [int(most_frequent_value_num + 5 * (self.num_player - 1) / 3),
                                  self.dice_dict[most_frequent_value_num-1], False]
                    print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1])
                    return self.guess
                # Try change and Zhai
                if self.dice_dict[real_most_frequent_value_num - 1] + 5 * (self.num_player - 1) / 6 > input_list[0] - 1:
                    self.guess = [int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 6),
                                  self.dice_dict[real_most_frequent_value_num-1], True]
                    print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # This AI think last guess is too big
                else:
                    print(self.player_id, '号玩家选择主动开！')
                    return [0, 0, False]  # Open


class QlearningAI(AI):
    pass


player_list = []

for player in range(NumPlayer):
    player_list.append(DumpAI())
    player_list[player].player_id = player + 1

state = [-1, 0, False]
guess = state
while True:
    for i in range(NumPlayer):
        player_list[i].ShowDice()
        state = player_list[i].Decide(state)
        if i == 0:
            guess = player_list[NumPlayer - 1].guess
        else:
            guess = player_list[i - 1].guess
        if state[0] == 0:
            break
    if state[0] == 0:
        total_dice = 0
        for i in range(NumPlayer):
            if guess[1] != 1:
                total_dice = int(player_list[i].dice_dict[guess[1] - 1]) + player_list[i].dice_dict[0] + total_dice
            else:
                total_dice = player_list[i].dice_dict[0] + total_dice
        if total_dice < guess[0]:
            print('开成功')
        else:
            print('开失败')
        break

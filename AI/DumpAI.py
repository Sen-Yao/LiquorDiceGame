import torch
import random

NumPlayer = 2


class AI:
    def __init__(self):
        """
        Initialize the base information

        """
        self.name = 'AI'
        self.num_player = NumPlayer
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

    def rename(self, name):
        self.name = name


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
        print(self.name, ' 玩家的骰子结果为', self.dice)

    def ShakeDice(self):
        self.dice = torch.randint(1, 7, (5,))
        self.dice = self.dice.sort()[0]
        unique_values = torch.unique(self.dice)
        # shake again
        while len(unique_values) == 5:
            self.dice = torch.randint(1, 7, (5,))
            unique_values = torch.unique(self.dice)
        self.second_dice = self.dice

    def Decide(self, input_list):
        """
        The AI will react depends on its dices result only
        :return: An action list
        """
        # Create a list to store the number of each number
        self.dice_dict = [0, 0, 0, 0, 0, 0]
        for i in self.dice:
            for j in range(6):
                if i == j + 1:
                    self.dice_dict[j] = self.dice_dict[j] + 1
        # Find the most frequent face in the dice
        unique_values, counts = torch.unique(self.dice, return_counts=True)
        most_frequent_value_face = 0
        most_frequent_value_num = 0
        real_most_frequent_value_face = 0
        real_most_frequent_value_num = 0

        if int(unique_values[counts.argmax()]) != 1:
            most_frequent_value_face = int(unique_values[counts.argmax()])
            real_most_frequent_value_face = int(unique_values[counts.argmax()])
            most_frequent_value_num = self.dice_dict[int(unique_values[counts.argmax()]) - 1] + self.dice_dict[0]
            real_most_frequent_value_num = self.dice_dict[int(unique_values[counts.argmax()]) - 1]
        # AI's most face is 1
        else:
            # Try to find out the second most face
            self.second_dice = self.dice[self.dice_dict[0] - 1:]
            second_unique_values, second_counts = torch.unique(self.second_dice, return_counts=True)
            most_frequent_value_face = int(second_unique_values[second_counts.argmax()])
            real_most_frequent_value_face = 1
            most_frequent_value_num = self.dice_dict[0]
            real_most_frequent_value_num = self.dice_dict[0]

        last_player_num = input_list[0]
        last_player_face = input_list[1]

        # For the face guessed by the last player, the number of dice that AI have
        # Zhai or 1
        if last_player_face == 1 or input_list[2]:
            respond_num = self.dice_dict[last_player_face - 1]
        else:
            respond_num = self.dice_dict[last_player_face - 1] + self.dice_dict[0]
        # print('debug:respond_num=', respond_num)
        # print('debug:most_frequent_value_num=', most_frequent_value_num)

        # This AI is the beginner
        if input_list[0] == -1:
            # AI has many 1
            if most_frequent_value_face == 1:
                self.guess = [NumPlayer, 1, False, self.name]
                print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1])
                return self.guess
            # AI has many real face, so it try to zhai
            if most_frequent_value_num - self.dice_dict[0] > 1:
                self.guess = [real_most_frequent_value_num + 5 * self.num_player // 6,
                              real_most_frequent_value_face, True, self.name]
                print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                return self.guess
            else:
                self.guess = [most_frequent_value_num + 5 * self.num_player // 3, most_frequent_value_face,
                              False, self.name]
                print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1])
                return self.guess
        # This AI is responding
        else:
            # Zhai or 1
            if (input_list[1] == 1) or input_list[2]:
                # This AI think he has enough same dice and won't be too dangerous to be opened
                if last_player_num - respond_num < (5 * (self.num_player - 1) / 6):
                    self.guess = [int(input_list[0] + 1), int(input_list[1]), True, self.name]
                    print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # Try Fei
                if self.dice_dict[input_list[1] - 1] < self.dice_dict[0] \
                        and self.dice_dict[input_list[1] - 1] + 5 * self.num_player / 3 > input_list[0]:
                    self.guess = [2 * input_list[0], int(input_list[1]), False, self.name]
                    print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1], '飞')
                    return self.guess
                # Try change
                if self.dice_dict[real_most_frequent_value_face - 1] + 5 * (self.num_player - 1) / 3 > input_list[0] - 1 \
                        and real_most_frequent_value_num != 1 \
                        and (int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 3) > input_list[0]
                             or (int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 3) == input_list[0]
                                 and self.dice_dict[real_most_frequent_value_face - 1] > input_list[1])):
                    self.guess = [int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 3),
                                  real_most_frequent_value_face, True, self.name]
                    print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # Try change and Fei
                if self.dice_dict[most_frequent_value_face - 1] + 5 * (self.num_player - 1) / 6 > input_list[0]:
                    self.guess = [int(most_frequent_value_num + 5 * (self.num_player - 1) / 6),
                                  self.dice_dict[most_frequent_value_face - 1], False, self.name]
                    print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1], '飞')
                    return self.guess
                # This AI think last input_guess is too big
                else:
                    print(self.name, ' 玩家选择主动开！')
                    return [0, 0, False]  # Open
            # Normal
            else:
                # This AI think he has enough same dice and won't be too dangerous to be opened
                if last_player_num - respond_num < (5 * (self.num_player - 1) / 3):
                    self.guess = [int(input_list[0] + 1), int(input_list[1]), False, self.name]
                    print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1])
                    return self.guess
                # Try Zhai
                if self.dice_dict[input_list[1] - 1] > self.dice_dict[0]:
                    self.guess = [int((input_list[0]) / 2 + 1), int(input_list[1]), True, self.name]
                    print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # Try change
                if (self.dice_dict[most_frequent_value_face - 1] + 5 * (self.num_player - 1) / 3 > input_list[0] - 1) \
                        and int(most_frequent_value_num + 5 * (self.num_player - 1) / 3) > input_list[0]:
                    self.guess = [int(most_frequent_value_num + 5 * (self.num_player - 1) / 3),
                                  self.dice_dict[most_frequent_value_face - 1], False, self.name]
                    print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1])
                    return self.guess
                # Try change and Zhai
                if self.dice_dict[real_most_frequent_value_face - 1] + 5 * (self.num_player - 1) / 6 > input_list[0]:
                    self.guess = [int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 6),
                                  self.dice_dict[real_most_frequent_value_face - 1], True, self.name]
                    print(self.name, ' 玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # This AI think last input_guess is too big
                else:
                    print(self.name, ' 玩家选择主动开！')
                    return [0, 0, False, self.name]  # Open


def judge_open(input_guess):
    total_dice = 0
    for i in range(NumPlayer):
        if input_guess[1] != 1 and not input_guess[2]:
            total_dice = int(player_list[i].dice_dict[input_guess[1] - 1]) + player_list[i].dice_dict[0] + total_dice
        if input_guess[2]:
            total_dice = int(player_list[i].dice_dict[input_guess[1] - 1]) + total_dice
        else:
            total_dice = player_list[i].dice_dict[0] + total_dice
    if total_dice < input_guess[0]:
        print('开成功')
    else:
        print('开失败')


def judge_legal_guess(last_guess, this_state):
    """
    Judge if a this_guess is legal
    :param last_guess: last this_guess made by previous player
    :param this_state: this this_guess made by this player
    :return: Bool value. True means legal.
    """
    if this_state[0] <= 0:
        return True
    if last_guess[2] == this_state[2]:
        if last_guess[0] < this_state[0]:
            return True
        if last_guess[0] == this_state[0] and last_guess[1] < this_state[0]:
            return True
    if last_guess[2]:
        if 2 * last_guess[0] > this_state[0]:
            return False
        else:
            return True
    if not last_guess[2]:
        if last_guess[0] // 2 > this_state[0]:
            return False
        else:
            return True


player_list = []


def train():
    for player in range(NumPlayer):
        player_list[player].player_id = player + 1

    state = [-1, 0, False, '']
    guess = state
    while True:
        for i in range(NumPlayer):
            player_list[i].ShowDice()
            temp_state = player_list[i].Decide(state)
            while not judge_legal_guess(state, temp_state):
                temp_state = player_list[i].Decide(state)
            state = temp_state
            if i == 0:
                guess = player_list[NumPlayer - 1].guess
            else:
                guess = player_list[i - 1].guess
            if state[0] == 0:
                break
        if state[0] == 0:
            judge_open(guess)
            break

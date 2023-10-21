import torch
from GameAI import AI


class DumpAI(AI):
    """
    A dump AI, base on traditional algorithm to generate a response.
    """

    def __init__(self, num_player, need_output=False):
        """
        Initialize the base information
        """
        super().__init__(num_player, need_output)

    def ShowDice(self):
        if self.need_output:
            print(self.name, '玩家的骰子结果为', self.dice)

    def Decide(self, input_list, ge, stuck):
        """
        The AI will react depends on its dices result only
        :return: An action list
        """
        # Find the most frequent face in the dice
        unique_values, counts = torch.unique(self.dice, return_counts=True)

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
                self.guess = [self.num_player, 1, False, self.name]
                if self.need_output:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                return self.guess
            # AI has many real face, so it try to zhai
            if most_frequent_value_num - self.dice_dict[0] > 1:
                self.guess = [real_most_frequent_value_num + 5 * self.num_player // 6,
                              real_most_frequent_value_face, True, self.name]
                if self.need_output:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                return self.guess
            else:
                self.guess = [most_frequent_value_num + 5 * self.num_player // 3, most_frequent_value_face,
                              False, self.name]
                if self.need_output:
                    print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                return self.guess
        # This AI is responding
        else:
            # Zhai or 1
            if (input_list[1] == 1) or input_list[2]:
                # This AI think he has enough same dice and won't be too dangerous to be opened
                if last_player_num - respond_num < (5 * (self.num_player - 1) / 6):
                    if input_list[1] != 1:
                        self.guess = [input_list[0] + 1, int(input_list[1]), True, self.name]
                        if self.need_output:
                            print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                        return self.guess
                    if input_list[1] == 1:
                        self.guess = [int(input_list[0] + 1), int(input_list[1]), False, self.name]
                        if self.need_output:
                            print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                        return self.guess
                # Try Fei
                if self.dice_dict[input_list[1] - 1] < self.dice_dict[0] \
                        and self.dice_dict[input_list[1] - 1] + 5 * self.num_player / 3 > input_list[0]:
                    self.guess = [2 * input_list[0], int(input_list[1]), False, self.name]
                    while self.guess[0] <= self.num_player:
                        self.guess[0] += 1
                    if self.need_output:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '飞')
                    return self.guess
                # Try change
                if self.dice_dict[real_most_frequent_value_face - 1] + 5 * (self.num_player - 1) / 6 > input_list[0] > \
                        self.dice_dict[input_list[1] - 1] + 5 * (self.num_player - 1) / 6 \
                        and real_most_frequent_value_face != 1 \
                        and real_most_frequent_value_face != input_list[1] \
                        and (int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 6) > input_list[0]
                             or (int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 6) == input_list[0]
                                 and real_most_frequent_value_face > input_list[1])):
                    self.guess = [int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 6),
                                  real_most_frequent_value_face, True, self.name]
                    if self.need_output:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # Try change and Fei
                if self.dice_dict[most_frequent_value_face - 1] + 5 * (self.num_player - 1) / 6 > 2 * input_list[0]:
                    self.guess = [int(most_frequent_value_num + 5 * (self.num_player - 1) / 6),
                                  self.dice_dict[most_frequent_value_face - 1], False, self.name]
                    if self.need_output:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '飞')
                    return self.guess
                # This AI think last input_guess is too big
                else:
                    if self.need_output:
                        print(self.name, '玩家选择主动开！')
                    return [0, 0, False]  # Open
            # Normal
            else:
                # This AI think he has enough same dice and won't be too dangerous to be opened
                if last_player_num - respond_num < (5 * (self.num_player - 1) / 3):
                    self.guess = [int(input_list[0] + 1), int(input_list[1]), False, self.name]
                    if self.need_output:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                    return self.guess
                # Try Zhai
                if self.dice_dict[input_list[1] - 1] > self.dice_dict[0] \
                        and input_list[0] - self.dice_dict[input_list[1] - 1] < 5 * self.num_player / 6:
                    self.guess = [int((input_list[0]) / 2 + 1), int(input_list[1]), True, self.name]
                    if self.need_output:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # Try change
                if (self.dice_dict[most_frequent_value_face - 1] + 5 * (self.num_player - 1) / 3 > input_list[0] - 1) \
                        and int(most_frequent_value_num + 5 * (self.num_player - 1) / 3) > input_list[0]:
                    self.guess = [int(most_frequent_value_num + 5 * (self.num_player - 1) / 3),
                                  self.dice_dict[most_frequent_value_face - 1], False, self.name]
                    if self.need_output:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
                    return self.guess
                # Try change and Zhai
                if self.dice_dict[real_most_frequent_value_face - 1] + 5 * (self.num_player - 1) / 6 > input_list[0]:
                    self.guess = [int(real_most_frequent_value_num + 5 * (self.num_player - 1) / 6),
                                  self.dice_dict[real_most_frequent_value_face - 1], True, self.name]
                    if self.need_output:
                        print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                    return self.guess
                # This AI think last input_guess is too big
                else:
                    if self.need_output:
                        print(self.name, '玩家选择主动开！')
                    return [0, 0, False, self.name]  # Open

import torch
import random
from DumpAI import AI, DumpAI

NumPlayer = 2
Learning_rate = 0.1
Discount_factor = 0.1
Epoch = 1000000

DEFAULT_GAME_CONFIG = {
    'game_num_players': 2
}


class QlearningAIOneLevel(AI):
    """
    An AI based on Q-learning algorithm to generate a response. It is a one level Q-learning, means that it will only
    consider the last input_guess to generate his response
    """

    def __init__(self, lr, df):
        """
        Initialize the base information
        """
        super().__init__()
        self.num_state = 12210 * self.num_player
        self.num_action = 55 * self.num_player + 1
        self.Q_table = torch.zeros((5 * self.num_player + 1, 6, 2, 6, 6, 6, 6, 6, 5 * self.num_player + 1, 6, 2))
        self.learning_rate = lr
        self.discount_factor = df
        self.greedy_epsilon = 0.1

    def ShowDice(self):
        print(self.player_id, '号玩家的骰子结果为', self.dice)

    def ShakeDice(self):
        self.dice = torch.randint(1, 7, (5,))
        self.dice = self.dice.sort()[0]
        unique_values = torch.unique(self.dice)
        # shake again
        while len(unique_values) == 5:
            self.dice = torch.randint(1, 7, (5,))
            unique_values = torch.unique(self.dice)
        self.second_dice = self.dice

    def update_Q(self, last_guess, this_guess, reward):
        Q_value = self.Q_table[last_guess[0]][last_guess[1]-1][int(last_guess[2])] \
            [int(self.dice[0])-1][int(self.dice[1])-1][int(self.dice[2])-1][int(self.dice[3])-1][int(self.dice[4])-1] \
            [this_guess[0]-1][this_guess[1]-1][int(this_guess[2])-1]
        print('debug:Q_value=', Q_value)
        Q_value = (1 - self.learning_rate) * Q_value + self.learning_rate * reward
        self.Q_table[last_guess[0]][last_guess[1] - 1][int(last_guess[2])] \
            [int(self.dice[0]) - 1][int(self.dice[1]) - 1][int(self.dice[2]) - 1][int(self.dice[3]) - 1][
            int(self.dice[4]) - 1] \
            [this_guess[0] - 1][this_guess[1] - 1][int(this_guess[2]) - 1]= Q_value

    def Decide(self, last_guess):
        """
        The AI will react depends on its dices result only
        :return: An action list
        """
        epsilon = random.random()
        # is greedy
        if epsilon < self.greedy_epsilon:
            return [random.randint(0, 5 * self.num_player), random.randint(0, 6), bool(random.randint(0, 1))]
        else:
            new_Q_table = self.Q_table[last_guess[0]][last_guess[1]-1][int(last_guess[2])]\
                [self.dice[0]-1][self.dice[1]-1][self.dice[2]-1][self.dice[3]-1][self.dice[4]-1]
            # Find the biggest Q in new_Q_table
            dim_0_biggest_Q, dim_0_biggest_index = torch.max(new_Q_table, dim=0)
            dim_1_biggest_Q, dim_1_biggest_index = torch.max(dim_0_biggest_Q, dim=0)
            dim_2_biggest_Q, dim_2_biggest_index = torch.max(dim_1_biggest_Q, dim=0)
            biggest_index = [int(dim_0_biggest_index[int(dim_1_biggest_index[0])][int(dim_2_biggest_index)]),
                             int(dim_1_biggest_index[int(dim_2_biggest_index)]), int(dim_2_biggest_index)]
            self.guess = biggest_index
            if self.guess[0] == 0:
                print(self.player_id, '号玩家选择开！')
                return self.guess
            if self.guess[2]:
                print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1], '斋')
                return self.guess
            else:
                print(self.player_id, '号玩家喊出', self.guess[0], '个', self.guess[1])
                return self.guess

    pass


def judge_open(input_guess):
    """
    Judge if an open to input_guess is legal
    :param input_guess:
    :return:
    """
    if input_guess[0] == -1 or input_guess[0] == 0:
        return False
    total_dice = 0
    for i in range(NumPlayer):
        if input_guess[1] != 1 and not input_guess[2]:
            total_dice = int(player_list[i].dice_dict[input_guess[1] - 1]) + player_list[i].dice_dict[0] + total_dice
        elif input_guess[2]:
            total_dice = int(player_list[i].dice_dict[input_guess[1] - 1]) + total_dice
        else:
            total_dice = player_list[i].dice_dict[0] + total_dice
    if total_dice < input_guess[0]:
        print('开成功')
        return True
    else:
        print('开失败')
        return False


def judge_legal_guess(last_guess, this_state):
    """
    Judge if this_guess is legal
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


def train(lr, df, epoch):

    for player in range(NumPlayer):
        player_list.append(DumpAI())
        player_list[player].player_id = player + 1
    player_list[0] = QlearningAIOneLevel(lr, df)
    for e in range(epoch):
        print('epoch=', e)
        for player in player_list:
            player.ShakeDice()
        state = [-1, 0, False]
        temp_state = state
        mark_state = state
        while True:
            for i in range(NumPlayer):
                player_list[i].ShowDice()
                # state is made by previous player
                # temp_state is made by this player, but not confirm yet
                # mark_state is made by previous player of the previous player, used to update Q of the previous player.
                temp_state = player_list[i].Decide(state)
                while not judge_legal_guess(state, temp_state):
                    if isinstance(player_list[i],QlearningAIOneLevel) :
                        player_list[i].update_Q(state, temp_state, -10)
                    temp_state = player_list[i].Decide(state)
                # state is an Open
                if temp_state[0] == 0:
                    break
                # Continue
                else:
                    if i == 0:
                        if player_list[i] is QlearningAIOneLevel:
                            player_list[0].update_Q(mark_state, state, 1)
                        state = player_list[NumPlayer - 1].guess
                    else:
                        if player_list[i] is QlearningAIOneLevel:
                            player_list[i-1].update_Q(mark_state, state, 1)
                        state = player_list[i - 1].guess

                mark_state = state
                state = temp_state

            if temp_state[0] == 0:
                # Open successful
                if judge_open(state) and player_list[i] is QlearningAIOneLevel:
                    player_list[i].update_Q(mark_state, state, -5)
                # Open unsuccessful
                else:
                    if (mark_state[0] == -1 or mark_state[0] == 0) and player_list[i] is QlearningAIOneLevel:
                        player_list[i].update_Q(mark_state, state, -10)
                    elif player_list[i] is QlearningAIOneLevel:
                        player_list[i].update_Q(mark_state, state, 2)
                break


train(Learning_rate, Discount_factor, Epoch)

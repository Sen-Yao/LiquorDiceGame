import torch
from DQN import DQN_agent
from Qlearning import QlearningAIOneLevel
from human import Human
from utils import judge_legal_guess, judge_open
import time

START_FACTOR = 0
ZHAI_FACTOR = 0.5
RANDOM_OPEN_FACTOR = 0.5

CONTINUE_REWARD = 25

BE_OPEN_REWARD = 40
BE_OPEN_PUNISH = -40

SUCCESSFUL_OPEN_REWARD = 40
UNSUCCESSFUL_OPEN_PUNISH = -52

ILLEGAL_PUNISH = -100


def play(targetAI, num_player, learning, save_learning_result, need_debug_info):
    """
    train main program.

    :param targetAI: The kind of AI that need to be trained
    :param num_player: The number of player during training
    :param learning:
    :param save_learning_result:
    :param need_debug_info: Whether you need output information for debug

    :return: None
    """
    player_list = [Human(num_player, need_debug_info)]
    player_list[0].name = 'player'
    for player in range(1, num_player):
        player_list.append(targetAI(num_player, need_debug_info))
        player_list[player].player_id = player + 1
        player_list[player].name = str(player + 1)

        if isinstance(player_list[1], QlearningAIOneLevel):
            try:
                player_list[1].Q_table = torch.load('model/QlearningOneLevel/num' + str(num_player) + '.pt')
                print('已读取 model/QlearningOneLevel/num' + str(num_player) + '.pth')
            except FileNotFoundError:
                torch.save(player_list[1].Q_table, 'model/QlearningOneLevel/num' + str(num_player) + '.pt')
        if isinstance(player_list[1], DQN_agent):
            try:
                player_list[1].net = torch.load('model/DQN/DQN.pkl')
                print('已读取 model/DQN/DQN.pkl')
            except FileNotFoundError:
                torch.save(player_list[1].net, 'model/DQN/DQN.pkl')

    win = 0
    i = 0
    print('正在开始……')
    for e in range(10000):
        print('\n第', e + 1, '局游戏开始！')
        if e == 0:
            i = 0
        for player in player_list:
            player.ShakeDice()
        state = [-1, 0, False]
        temp_state = [-1, 1, False]
        mark_state = [-1, 2, False]
        while True:
            while i < num_player:
                # Don't need stuck is a normal game, so initialize the generator
                # If player don't need stuck, it is either coach or a target AI finished it's stuck
                greedy = 0
                temp_state = player_list[i].Decide(state, greedy)
                while not judge_legal_guess(state, temp_state, num_player):
                    if need_debug_info:
                        print(temp_state, '不是一个合法猜测！')
                    if learning and i != 0:
                        player_list[i].SingleActionUpdate(state, temp_state, ILLEGAL_PUNISH, 0.01)
                    greedy += 0.1
                    temp_state = player_list[i].Decide(state, greedy)
                # the new guess is an Open
                if temp_state[0] == 0:
                    print(player_list[i].name, '开了！！')
                    # Open successful
                    if judge_open(state, num_player, player_list):
                        time.sleep(2)
                        if i != 0:
                            print('开成功了！您输了！')
                            if learning:
                                player_list[i].SingleActionUpdate(state, temp_state, SUCCESSFUL_OPEN_REWARD, 0.01)
                        else:
                            print(player_list[i].name, '开成功了！您赢了！')
                            win += 1
                            if learning:
                                player_list[num_player-1].SingleActionUpdate(mark_state, state, BE_OPEN_PUNISH, 0.01)
                        print('大家的骰子为：')
                        for player in player_list:
                            print(player.name, player.dice.tolist())
                        print('\n\n')
                        time.sleep(2)
                        break
                    # Open unsuccessful
                    else:
                        time.sleep(2)
                        if i != 0:
                            print('开失败了！您赢了！')
                            win += 1
                            if learning:
                                player_list[i].SingleActionUpdate(state, temp_state, UNSUCCESSFUL_OPEN_PUNISH, 0.01)
                        else:
                            print(player_list[i].name, '开失败了！您输了！')
                            if learning:
                                player_list[num_player-1].SingleActionUpdate(mark_state, state, BE_OPEN_REWARD, 0.01)
                        print('大家的骰子为：')
                        for player in player_list:
                            print(player.name, player.dice.tolist())
                        print('\n\n')
                        time.sleep(2)
                        break
                else:
                    if learning:
                        if i == 0 and state[0] != -1:
                            player_list[num_player-1].SingleActionUpdate(state, temp_state, CONTINUE_REWARD, 0.01)
                mark_state = state.copy()
                state = temp_state.copy()

                if i == num_player - 1:
                    i = 0
                else:
                    i += 1
            if temp_state[0] == 0:
                break
        print('当前您的胜率为', 100 * win / (e+1), '%')
        if save_learning_result:
            if isinstance(player_list[1], DQN_agent):
                torch.save(player_list[1].net, 'model/DQN/DQN.pkl')
                print('\n\n\n\n已保存训练结果\n\n')

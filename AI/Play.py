import torch
from GameAI import AI
from DQN import DQN_agent
from Qlearning import QlearningAIOneLevel
from human import Human
from utils import judge_legal_guess, judge_open
import time


def play(targetAI, num_player, need_debug_info):
    """
    train main program.

    :param use_stuck:
    :param is_game:
    :param targetAI: The kind of AI that need to be trained
    :param num_player: The number of player during training
    :param need_debug_info: Whether you need output information for debug
    :param lr: Learning Rate
    :param df: Discount Factor
    :param ge: Greedy Epsilon
    :param epoch: Training Epoch
    :param coachAI: The kind of AI that coach the targetAI
    :return: None
    """
    player_list = [Human(num_player, 0, need_debug_info)]
    player_list[0].name = 'player'
    for player in range(1, num_player):
        player_list.append(targetAI(num_player, 0, need_debug_info))
        player_list[player].player_id = player + 1
        player_list[player].name = str(player + 1)

        if isinstance(player_list[1], QlearningAIOneLevel):
            try:
                player_list[1].Q_table = torch.load('model/QlearningOneLevel/num' + str(num_player) + '.pt')
                print('已读取model/QlearningOneLevel/num' + str(num_player) + '.pth')
            except Exception:
                torch.save(player_list[1].Q_table, 'model/QlearningOneLevel/num' + str(num_player) + '.pt')
        if isinstance(player_list[1], DQN_agent):
            try:
                player_list[1].net = torch.load('model/DQN/test.pkl')
                print('已读取 model/DQN/test.pkl')
            except Exception:
                torch.save(player_list[1].net, 'model/DQN/test.pkl')

    win = 0
    print('正在开始……')
    for e in range(10000):
        print('\n第', e + 1, '局游戏开始！')
        for player in player_list:
            player.ShakeDice()
        state = [-1, 0, False]
        temp_state = [-1, 1, False]
        i = 0
        while True:
            while i < num_player:
                # Don't need stuck is a normal game, so initialize the generator
                # If player don't need stuck, it is either coach or a target AI finished it's stuck
                greedy = 0
                temp_state = player_list[i].Decide(state, greedy)
                while not judge_legal_guess(state, temp_state, num_player):
                    if need_debug_info:
                        print(temp_state, '不是一个合法猜测！')
                    greedy += 0.1
                    temp_state = player_list[i].Decide(state, greedy + 0.1)
                # the new guess is an Open
                if temp_state[0] == 0:
                    print(player_list[i].name, '开了！！')
                    # Open successful
                    if judge_open(state, num_player, player_list):
                        time.sleep(2)
                        if i != 0:
                            print('开成功了！您输了！')
                        else:
                            print(player_list[i].name, '开成功了！您赢了！')
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
                        else:
                            print(player_list[i].name, '开失败了！您输了！')
                        print('大家的骰子为：')
                        for player in player_list:
                            print(player.name, player.dice.tolist())
                        print('\n\n')
                        time.sleep(2)
                        break
                state = temp_state
                if i == num_player - 1:
                    i = 0
                else:
                    i += 1
            if temp_state[0] == 0:
                break

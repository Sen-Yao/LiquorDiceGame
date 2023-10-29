import random

import torch
from DQN import DQN_agent
from Qlearning import QlearningAIOneLevel
from utils import judge_legal_guess, judge_open
from ClassicAI import ClassicAI
import time

CONTINUE_REWARD = 25

BE_OPEN_REWARD = 40
BE_OPEN_PUNISH = -40

SUCCESSFUL_OPEN_REWARD = 40
UNSUCCESSFUL_OPEN_PUNISH = -52

ILLEGAL_PUNISH = -100


def output_train_info(target, epoch, win, last_output_time, last_output_epoch):
    if time.time() - last_output_time > 5:
        if isinstance(target, QlearningAIOneLevel):
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), 'epoch=', epoch,
                  '训练速度为', (epoch - last_output_epoch) / 5, 'epoch / s'
                                                                 '最近胜率为',
                  float(100 * win / epoch - last_output_epoch), '%', '发现了', target.zero_detect, '次 Q 值为零')
            target.zero_detect = 0
        if isinstance(target, DQN_agent):
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), 'epoch=', epoch,
                  '训练速度为', (epoch - last_output_epoch) / 5, 'epoch / s',
                  '最近胜率为', float(100 * win / (epoch - last_output_epoch)), '%')
        return True
    else:
        return False


def load_target(target, num_player, need_output):
    if isinstance(target, QlearningAIOneLevel):
        try:
            target.Q_table = torch.load('model/QlearningOneLevel/num' + str(num_player) + '.pt')
            if need_output:
                print('已读取model/QlearningOneLevel/num' + str(num_player) + '.pt')
        except FileNotFoundError:
            torch.save(target.Q_table, 'model/QlearningOneLevel/num' + str(num_player) + '.pt')
    if isinstance(target, DQN_agent):
        try:
            target.net = torch.load('model/DQN/DQN.pkl')
            if need_output:
                print('已读取model/DQN/DQN.pkl')
        except FileNotFoundError:
            torch.save(target.net, 'model/DQN/DQN.pkl')
    pass


def save_target(target, num_player, last_save_time):
    if time.time() - last_save_time > 30:
        if isinstance(target, QlearningAIOneLevel):
            torch.save(target.Q_table, 'model/QlearningOneLevel/num' + str(num_player) + '.pt')
            print('已保存')
        if isinstance(target, DQN_agent):
            torch.save(target.net, 'model/DQN/DQN.pkl')
            print('已保存')
        return True
    else:
        return False


def train(targetAI, coachAI, learning_rate, greedy_epsilon, max_epoch, num_player, need_debug_info):
    """
    train main program, Use real game for trainable AI to train.

    :param targetAI: The kind of AI that need to be trained
    :param num_player: The number of player during training
    :param need_debug_info: Whether you need output information for debug
    :param learning_rate: Learning Rate
    :param greedy_epsilon: Greedy Epsilon
    :param max_epoch: Training Epoch
    :param coachAI: The kind of AI that coach the targetAI

    :return: None
    """

    win = 0
    last_output_time = time.time()
    last_save_time = time.time()
    last_output_epoch = 0

    print('正在开始……')
    for e in range(max_epoch):

        coach_list = [ClassicAI, QlearningAIOneLevel, DQN_agent]

        player_list = [targetAI(num_player, need_debug_info)]
        load_target(player_list[0], num_player, False)
        # Add a bunch of coach AI
        for player in range(1, num_player):
            player_list.append(random.choice(coach_list)(num_player, need_debug_info))
            player_list[player].player_id = player + 1
            player_list[player].name = '陪练' + str(player + 1)
            load_target(player_list[player], num_player, False)

        # Output information
        if output_train_info(player_list[0], e, win, last_output_time, last_output_epoch):
            last_output_time = time.time()
            last_output_epoch = e
            win = 0

        # Save and Update
        if save_target(player_list[0], num_player, last_save_time):
            last_save_time = time.time()
            for player in player_list:
                load_target(player, num_player, False)

        if need_debug_info:
            print('\n\n\nepoch=', e)

        for player in player_list:
            player.ShakeDice()

        state = [-1, 0, False]
        temp_state = [-1, 1, False]
        mark_state = [-1, 2, False]
        # state is made by previous player
        # temp_state is made by this player, but not confirm yet
        # mark_state is made by previous player of the previous player,
        # used to GetReward of the previous player.

        while True:
            for i in range(num_player):
                player_list[i].ShowDice()
                temp_state = player_list[i].Decide(state, greedy_epsilon)

                # Ask for guess until temp_state is a legal guess
                while not judge_legal_guess(state, temp_state, num_player):
                    if need_debug_info:
                        print(temp_state, '不是一个合法猜测！')
                    if isinstance(player_list[i], targetAI):
                        player_list[i].SingleActionUpdate(state, temp_state, ILLEGAL_PUNISH, learning_rate)
                        if need_debug_info:
                            print('收到-100的惩罚')
                    temp_state = player_list[i].Decide(state, greedy_epsilon)

                # the new guess is an Open
                if temp_state[0] == 0:
                    if need_debug_info:
                        print(player_list[i].name, '开了！！')
                    # Open successful
                    if judge_open(state, num_player, player_list):
                        if need_debug_info:
                            print(player_list[i].name, '开成功了！')
                            print('大家的骰子为：')
                            for player in player_list:
                                print(player.name, player.dice.tolist())
                            print('\n\n')
                        if isinstance(player_list[i], targetAI) and i == 0:
                            if need_debug_info:
                                print(player_list[i].name, '在', state, '下选择', temp_state, '受到了奖励')
                            player_list[i].SingleActionUpdate(state, temp_state, SUCCESSFUL_OPEN_REWARD, learning_rate)
                            win += 1
                            break
                        # If AI that make error guess is target AI, then need punish
                        if i == 1:
                            if isinstance(player_list[0], targetAI):
                                if need_debug_info:
                                    print(player_list[0].name, '在', mark_state, '下选择', state,
                                          '受到了惩罚')
                                player_list[0].SingleActionUpdate(mark_state, state, BE_OPEN_PUNISH, learning_rate)
                                mark_state = state
                                state = temp_state
                                i += 1
                                continue
                        else:
                            mark_state = state
                            state = temp_state
                            i += 1
                        break
                    # Open unsuccessful
                    else:
                        if need_debug_info:
                            print(player_list[i].name, '开失败了！')
                            print('大家的骰子为：')
                            for player in player_list:
                                print(player.name, player.dice.tolist())
                            print('\n\n')
                        # Punish AI
                        # open the initial
                        if state[0] < 1 and isinstance(player_list[i], targetAI) and i == 0:
                            if need_debug_info:
                                print('开到初始值了！')
                            player_list[0].SingleActionUpdate(state, temp_state, ILLEGAL_PUNISH, learning_rate)
                        # Normal error open
                        else:
                            # Punish AI
                            if isinstance(player_list[0], targetAI) and i == 0:
                                if need_debug_info:
                                    print(player_list[i].name, '在', state, '下选择', temp_state, '受到了惩罚')
                                player_list[0].SingleActionUpdate(state, temp_state, UNSUCCESSFUL_OPEN_PUNISH,
                                                                  learning_rate)
                            # Reward last AI
                            if i == 1:
                                if isinstance(player_list[0], targetAI):
                                    if need_debug_info:
                                        print(player_list[0].name, '在', mark_state, '下选择', state,
                                              '受到了奖励')
                                    player_list[0].SingleActionUpdate(mark_state, state, BE_OPEN_REWARD, learning_rate)
                            mark_state = state
                            state = temp_state
                            win += 1
                            break
                # Continue
                else:
                    # This player choose continue, means previous player (maybe AI) survived, deserve a reward
                    if i == 1 and state != -1:
                        if isinstance(player_list[0], targetAI):
                            player_list[0].SingleActionUpdate(mark_state, state, CONTINUE_REWARD, learning_rate)
                            if need_debug_info:
                                print(player_list[0].name, '因为逃过一劫获得了 10 的奖励')
                mark_state = state
                state = temp_state
            if temp_state[0] == 0:
                break

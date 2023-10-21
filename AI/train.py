import torch
from GameAI import AI
from DumpAI import DumpAI
from DQN import DQN_agent
from Qlearning import QlearningAIOneLevel
from utils import judge_legal_guess, judge_open
import time


def trainDQN(targetAI, num_player, need_output, lr, df, ge, epoch, coachAI, is_game=False, use_stuck=False):
    """
    train main program.

    :param is_game:
    :param targetAI: The kind of AI that need to be trained
    :param num_player: The number of player during training
    :param need_output: Whether you need output information for debug
    :param lr: Learning Rate
    :param df: Discount Factor
    :param ge: Greedy Epsilon
    :param epoch: Training Epoch
    :param coachAI: The kind of AI that coach the targetAI
    :return: None
    """
    player_list = []
    for player in range(num_player):
        player_list.append(coachAI(num_player, need_output))
        player_list[player].player_id = player + 1
        player_list[player].name = str(player + 1)
        if isinstance(player_list[player], QlearningAIOneLevel):
            try:
                player_list[player].Q_table = torch.load('model/QlearningOneLevel/num' + str(num_player) + '.pt')
            except Exception:
                torch.save(player_list[player].Q_table, 'model/QlearningOneLevel/num' + str(num_player) + '.pt')
        player_list[player].need_stuck = False
        player_list[player].allow_stuck = False
    player_list[0] = targetAI(num_player, need_output)
    if is_game or not use_stuck:
        player_list[0].need_stuck = False
        player_list[0].allow_stuck = False
    if isinstance(player_list[0], QlearningAIOneLevel):
        try:
            player_list[0].Q_table = torch.load('model/QlearningOneLevel/num' + str(num_player) + '.pt')
        except Exception:
            torch.save(player_list[0].Q_table, 'model/QlearningOneLevel/num' + str(num_player) + '.pt')
    if isinstance(player_list[0], DQN_agent):
        try:
            player_list[0].net.load_state_dict(torch.load('model/DQN/num' + str(num_player) + '.pth'))
        except Exception:
            torch.save(player_list[0].net.state_dict(), 'model/DQN/num' + str(num_player) + '.pth')

    if is_game:
        player_list[1].name = 'player'

    win = 0
    print('正在开始……')
    for e in range(epoch):
        if is_game:
            print('\n第', e+1, '局游戏开始！')
        player_list[0].epoch = e
        if e % 100 == 99 and isinstance(player_list[0], QlearningAIOneLevel) and use_stuck:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), 'epoch=', epoch, '近一百场胜率为',
                  float(win / 1), '%', '发现了', player_list[0].zero_detect, '次 Q 值为零')
            player_list[0].zero_detect = 0
            win = 0
        if e % 10000 == 9999 and isinstance(player_list[0], QlearningAIOneLevel) and not use_stuck:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), 'epoch=', epoch, '近一百场胜率为',
                  float(win / 1), '%', '发现了', player_list[0].zero_detect, '次 Q 值为零')
            player_list[0].zero_detect = 0
            win = 0
        if (e % 1000 == 999 or is_game) and use_stuck:
            if isinstance(player_list[0], QlearningAIOneLevel):
                torch.save(player_list[0].Q_table, 'model/QlearningOneLevel/num' + str(num_player) + '.pt')
                print('已保存')
                for player in player_list:
                    if isinstance(player, QlearningAIOneLevel):
                        player.Q_table = torch.load('model/QlearningOneLevel/num' + str(num_player) + '.pt')
        if e % 100000 == 99999 or is_game and not use_stuck:
            if isinstance(player_list[0], QlearningAIOneLevel):
                torch.save(player_list[0].Q_table, 'model/QlearningOneLevel/num' + str(num_player) + '.pt')
                print('已保存')
                for player in player_list:
                    if isinstance(player, QlearningAIOneLevel):
                        player.Q_table = torch.load('model/QlearningOneLevel/num' + str(num_player) + '.pt')
        if e % 1000 == 999 and isinstance(player_list[0], DQN_agent):
            torch.save(player_list[0].net.state_dict(), 'model/DQN/num' + str(num_player) + '.pth')
            print('已保存')
        if need_output:
            print('\n\n\nepoch=', e)
        for player in player_list:
            player.ShakeDice()
        state = [-1, 0, False]
        temp_state = [-1, 1, False]
        mark_state = [-1, 2, False]
        guess = None
        target_guess = None
        while True:
            i = 0
            while i < num_player:
                player_list[i].ShowDice()
                # Don't need stuck is a normal game, so initialize the generator
                # If player don't need stuck, it is either coach or a target AI finished it's stuck

                if not player_list[i].need_stuck:
                    # It is a target AI, and it has output a valid guess, so now it needs to rebuild generator
                    if isinstance(player_list[i], targetAI):
                        target_guess = player_list[i].Decide(state, ge)
                        temp_state = next(target_guess)
                    # It is a coach
                    else:
                        guess = player_list[i].Decide(state, ge)
                        temp_state = next(guess)
                # It is a target AI, and it is still stuck
                else:
                    temp_state = next(target_guess)
                # state is made by previous player
                # temp_state is made by this player, but not confirm yet
                # mark_state is made by previous player of the previous player,
                # used to GetReward of the previous player.
                # Ask for guess until temp_state is a legal guess
                while not judge_legal_guess(state, temp_state, num_player):
                    if need_output:
                        print(temp_state, '不是一个合法猜测！')
                    if isinstance(player_list[i], targetAI):
                        player_list[i].GetReward(state, temp_state, -100, lr, is_game)
                        if need_output:
                            print('收到-100的惩罚')
                        temp_state = next(target_guess)
                    else:
                        temp_state = next(guess)
                # the new guess is an Open
                if temp_state[0] == 0:
                    if is_game or need_output:
                        print(player_list[i].name, '开了！！')
                    # Open successful
                    if judge_open(state, num_player, player_list):
                        if is_game or need_output:
                            if is_game:
                                if i != 0:
                                    print('开成功了！您赢了！')
                                else:
                                    print(player_list[i].name, '开成功了！您输了！')
                            else:
                                print(player_list[i].name, '开成功了！')
                            print('大家的骰子为：')
                            for player in player_list:
                                print(player.name, player.dice.tolist())
                            print('\n\n')
                        if isinstance(player_list[i], targetAI) and i == 0:
                            if need_output:
                                print(player_list[i].name, '在', state, '下选择', temp_state, '受到了奖励')
                            player_list[i].GetReward(state, temp_state, 20, lr, is_game)
                            if player_list[i].need_stuck:
                                temp_state = state
                                state = mark_state
                                i = num_player - 1
                                if need_output:
                                    print('时光倒流！')
                            else:
                                win += 1
                                break
                        # Punish last AI
                        if i == 1:
                            if isinstance(player_list[0], targetAI):
                                if need_output:
                                    print(player_list[0].name, '在', mark_state, '下选择', state,
                                          '受到了惩罚')
                                player_list[0].GetReward(mark_state, state, -50, lr, is_game)
                                if player_list[0].need_stuck:
                                    temp_state = state
                                    state = mark_state
                                    i -= 1
                                    if need_output:
                                        print('时光倒流！')
                                else:
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
                        if is_game or need_output:
                            if is_game:
                                if i != 0:
                                    print('开失败了！您输了！')
                                else:
                                    print(player_list[i].name, '开失败了！您赢了！')
                            else:
                                print(player_list[i].name, '开失败了！')
                            print('大家的骰子为：')
                            for player in player_list:
                                print(player.name, player.dice.tolist())
                            print('\n\n')
                        # Punish AI
                        # open the initial
                        if state[0] < 1 and isinstance(player_list[i], targetAI) and i == 0:
                            if need_output:
                                print('开到初始值了！')
                            player_list[0].GetReward(state, temp_state, -100, lr, is_game)

                        # Normal error open
                        else:
                            # Punish AI
                            if isinstance(player_list[i], targetAI) and i == 0:
                                # print('GetReward Q =', player_list[i].GetReward_Q)
                                if need_output:
                                    print(player_list[i].name, '在', state, '下选择', temp_state, '受到了惩罚')
                                player_list[i].GetReward(state, temp_state, -50, lr, is_game)
                            # Reward last AI
                            if i == 1:
                                if isinstance(player_list[0], targetAI):
                                    if need_output:
                                        print(player_list[0].name, '在', mark_state, '下选择', state,
                                              '受到了奖励')
                                    player_list[0].GetReward(mark_state, state, 20, lr, is_game)

                            if player_list[0].need_stuck:
                                temp_state = state
                                state = mark_state
                                i -= 1
                                if need_output:
                                    print('时光倒流！')
                                continue
                            else:
                                mark_state = state
                                state = temp_state
                                i += 1
                                win += 1
                                break
                # Continue
                else:
                    # This player choose continue, means previous player (maybe AI) survived, deserve a reward
                    # print('mark_state and state', mark_state, state)
                    if i == 1:
                        if isinstance(player_list[0], targetAI):
                            player_list[0].GetReward(mark_state, state, 10, lr, is_game)
                            if need_output:
                                print(player_list[0].name, '因为逃过一劫获得了 10 的奖励')
                        if player_list[0].need_stuck:
                            temp_state = state
                            state = mark_state
                            i -= 1
                            if need_output:
                                print('时光倒流！\n\n')

                        else:
                            mark_state = state
                            state = temp_state
                            i += 1
                        continue
                    else:
                        mark_state = state
                        state = temp_state
                        i += 1
                    continue
            if temp_state[0] == 0:
                # open successful
                for player in player_list:
                    player.need_stuck = False
                break

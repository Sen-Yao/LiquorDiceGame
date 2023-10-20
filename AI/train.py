import torch
from GameAI import AI
from DumpAI import DumpAI
from Qlearning import QlearningAIOneLevel
from utils import judge_legal_guess, judge_open


def train(targetAI, num_player, need_output, lr, df, ge, epoch, coachAI, is_game=False):
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
        if isinstance(coachAI, QlearningAIOneLevel):
            try:
                player_list[player].Q_table = torch.load('tensor/num'+str(num_player)+'.pt')
            except AttributeError:
                torch.save(player_list[player].Q_table, 'tensor/num' + str(num_player) + '.pt')
    player_list[0] = targetAI(num_player, need_output)
    if is_game:
        player_list[1].name = 'player'
    # torch.save(player_list[0].Q_table, 'tensor/tensor1.pt')
    # torch.save(player_list[1].Q_table, 'tensor/tensor2.pt')
    win = 0
    for e in range(epoch):
        if e % 10000 == 9999:
            print('近一万场胜率为', float(win / 100), '%')
            win = 0
        if e % 100000 == 0 or is_game:
            print('已保存')
            torch.save(player_list[0].Q_table, 'tensor/num'+str(num_player)+'.pt')
            if not is_game:
                if isinstance(player_list[1], QlearningAIOneLevel):
                    torch.save(player_list[1].Q_table, 'tensor/tensor2.pt')
            print('大小为', player_list[0].Q_table.untyped_storage().size())
        if need_output:
            print('\n\n\nepoch=', e)
        for player in player_list:
            player.ShakeDice()
        state = [-1, 0, False]
        temp_state = [-1, 1, False]
        mark_state = [-1, 2, False]
        # print('mark_state', mark_state)
        while True:
            i = 0
            for i in range(num_player):
                player_list[i].ShowDice()
                # state is made by previous player
                # temp_state is made by this player, but not confirm yet
                # mark_state is made by previous player of the previous player, used to update Q of the previous player.
                temp_state = player_list[i].Decide(state, ge)
                # illegal guess
                while not judge_legal_guess(state, temp_state, num_player):
                    if isinstance(player_list[i], targetAI):
                        player_list[i].update_Q(state, temp_state, -100, lr, is_game)
                    temp_state = player_list[i].Decide(state, ge)

                # state is an Open
                if temp_state[0] == 0:
                    break
                # Continue
                else:
                    # This player choose continue, means previous player (maybe AI) survived, deserve a reward
                    # print('mark_state and state', mark_state, state)
                    if mark_state[0] != -1:
                        if i == 0:
                            if isinstance(player_list[num_player - 1], targetAI):
                                player_list[num_player - 1].update_Q(mark_state, state, 10, lr, is_game)
                        else:
                            if isinstance(player_list[i - 1], targetAI):
                                player_list[i - 1].update_Q(mark_state, state, 10, lr, is_game)
                mark_state = state
                state = temp_state
                # print('state change to', temp_state)

            if temp_state[0] == 0:
                # open successful
                if judge_open(state, num_player, player_list):
                    if is_game or need_output:
                        print('开成功了！')
                        if i == 0:
                            print('对方的骰子为', player_list[num_player - 1].dice)
                        else:
                            print('对方的骰子为', player_list[i - 1].dice)
                        print('\n\n\n')
                    if isinstance(player_list[i], targetAI):
                        if need_output:
                            print(player_list[i].name, '在', state, '下选择', temp_state, '受到了奖励')
                        player_list[i].update_Q(state, temp_state, 20, lr, is_game)
                        win += 1

                    # Punish last AI
                    if i == 0:
                        if isinstance(player_list[num_player - 1], targetAI):
                            if need_output:
                                print(player_list[num_player - 1].name, '在', mark_state, '下选择', state, '受到了惩罚')
                            player_list[num_player - 1].update_Q(mark_state, state, -50, lr, is_game)
                    else:
                        if isinstance(player_list[i - 1], targetAI):
                            if need_output:
                                print(player_list[i - 1].name, '在', mark_state, '下选择', state, '受到了惩罚')
                            player_list[i - 1].update_Q(mark_state, state, -50, lr, is_game)

                    break
                # Open unsuccessful
                else:
                    if is_game or need_output:
                        print('开失败了！')
                        if i == 0:
                            print('对方的骰子为', player_list[num_player - 1].dice)
                        else:
                            print('对方的骰子为', player_list[i - 1].dice)
                        print('\n\n\n')
                    # Punish AI
                    # open the initial
                    if state[0] < 1 and isinstance(player_list[i], targetAI):
                        if need_output:
                            print('开到初始值了！', state, temp_state)
                        player_list[i].update_Q(state, temp_state, -100, lr, is_game)
                        break
                    # Normal error open
                    else:
                        if isinstance(player_list[i], targetAI):
                            # print('update Q =', player_list[i].update_Q)
                            if need_output:
                                print(player_list[i].name, '在', state, '下选择', temp_state, '受到了惩罚')
                            player_list[i].update_Q(state, temp_state, -50, lr, is_game)
                        if i == 0:
                            # Reward last AI
                            if isinstance(player_list[num_player - 1], targetAI):
                                if need_output:
                                    print(player_list[num_player - 1].name, '在', mark_state, '下选择', state,
                                          '受到了奖励')
                                player_list[i].update_Q(mark_state, state, 20, lr, is_game)
                                win += 1
                        else:
                            if isinstance(player_list[i - 1], targetAI):
                                if need_output:
                                    print(player_list[i - 1].name, '在', mark_state, '下选择', state, '受到了奖励')
                                player_list[i - 1].update_Q(mark_state, state, 20, lr, is_game)
                                win += 1
                        break

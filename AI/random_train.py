import random
import torch
import time
from GameAI import AI
from Qlearning import QlearningAIOneLevel
from DQN import DQN_agent, try_gpu
from utils import judge_legal_guess, judge_open

START_FACTOR = 0.5
ZHAI_FACTOR = 0.75


def RandomTrain(targetAI, coachAI, learning_rate, greedy_epsilon, max_epoch, max_player_num, need_debug_info):
    player_list = [targetAI(2, learning_rate, need_debug_info), coachAI(2, need_debug_info)]
    player_list[0].name = 'Target'
    player_list[1].name = 'Coach'
    if isinstance(player_list[0], DQN_agent):
        try:
            player_list[0].net = torch.load('model/DQN/test.pkl')
            player_list[0].net = player_list[0].net.to(device=try_gpu())
            if isinstance(player_list[1], DQN_agent):
                player_list[1].net = player_list[0].net
            print('成功读取 model/DQN/test.pkl')
        except FileNotFoundError:
            torch.save(player_list[0].net, 'model/DQN/test.pkl')
    print('正在开始训练，请稍后...')
    for epoch in range(max_epoch):
        # Generate player's number
        player_num = random.randint(2, max_player_num)
        if need_debug_info:
            print('\n\n\n本局游戏玩家数为', player_num)
        player_list[0].num_player = player_num
        player_list[1].num_player = player_num
        player_list = player_list[:2]
        for num in range(2, player_num):
            player_list.append(AI(player_num, need_debug_info))
        # Generate state
        init_random_factor = random.random()
        # target is a start
        if init_random_factor < START_FACTOR:
            if need_debug_info:
                print('由 Target 来做出第一个猜测')
            init_guess = [-1, 0, False]
            player_list[0].ShakeDice()
            Traverse_target_decide(player_list[0], player_list[1], player_list,
                                   init_guess, learning_rate, greedy_epsilon, need_debug_info)
        else:
            # Make a reasonable but random guess for target to continue
            if init_random_factor < ZHAI_FACTOR:
                # Init guess is Fei
                init_guess = [random.randint(player_num, player_num + 3), random.randint(2, 6), False]
                if need_debug_info:
                    print('Init 为', init_guess)
            else:
                # Init guess is Zhai
                init_guess = [random.randint(player_num // 2, player_num // 2 + 3), random.randint(2, 6), True]
                if need_debug_info:
                    print('Init 为', init_guess)
            player_list[1].ShakeDice()

            last_guess = player_list[1].Decide(init_guess, greedy_epsilon)
            while (not judge_legal_guess(init_guess, last_guess, player_num)) or last_guess[0] == 0:
                if need_debug_info:
                    print('last player 做出了一个不合法的猜测', last_guess)
                last_guess = player_list[1].Decide(init_guess, greedy_epsilon + 0.1)
            player_list[0].ShakeDice()
            Traverse_target_decide(player_list[0], player_list[1], player_list,
                                   last_guess, learning_rate, greedy_epsilon, need_debug_info)
        if epoch % 2000 == 0 and epoch != 0:
            if isinstance(player_list[0], DQN_agent):
                torch.save(player_list[0].net, 'model/DQN/test.pkl')
                print('\n\n\n\n已保存训练结果\n\n')
            if isinstance(player_list[1], DQN_agent):
                player_list[1].net = player_list[0].net
                print('已更新训练数据集\n\n\n\n')

        if epoch % 200 == 0:
            player_list[0].avg_loss = player_list[0].avg_loss \
                                      / (player_list[0].update_time * player_list[0].length_of_guess_vector)
            player_list[0].decide_loss = player_list[0].decide_loss / player_list[0].decide_try
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                  'epoch =', epoch,
                  'loss=', float(player_list[0].avg_loss),
                  '，平均决策误差为', player_list[0].decide_loss)
            player_list[0].update_time = 0
            player_list[0].decide_loss = 0.0
            player_list[0].decide_try = 0
            player_list[0].avg_loss = 0


def Traverse_target_decide(target, coach, player_list, last_guess, learning_rate, greedy_epsilon, need_debug_info):
    """
    Traverse all possible decide for target AI, and generate reward factor

    :param target:
    :param coach:
    :param player_list:
    :param last_guess:
    :param learning_rate:
    :param greedy_epsilon:
    :param need_debug_info:
    :return:
    """
    target_decide = [0, 0, False]
    for target_guess_num in range(6):
        # target decide to open
        if target_guess_num == 5:
            if last_guess[0] == -1:
                if need_debug_info:
                    print('Target 开了初始值!')
                    target_decide[0] = 0
                    target.GetReward(last_guess, target_decide, -99, learning_rate)
            else:
                if need_debug_info:
                    print('Target 选择开')
                target_decide[0] = 0
                if not judge_open(last_guess, len(player_list), player_list, need_debug_info):
                    target.GetReward(last_guess, target_decide, -99, learning_rate)
                else:
                    target.GetReward(last_guess, target_decide, 30, learning_rate)
            break

        # Target decide to continue
        for target_guess_face in range(1, 7):
            for target_guess_zhai in range(2):

                # Reformulate the target_decide
                target_decide[1] = target_guess_face
                target_decide[2] = bool(target_guess_zhai)
                if last_guess[0] == -1:
                    target_decide[0] = len(player_list) + target_guess_num
                # last is fei, and now target decide to zhai or 1
                elif (last_guess[1] != 1 and not last_guess[2]) and (target_guess_face == 1 or target_guess_zhai):
                    target_decide[0] = last_guess[0] // 2 + target_guess_num
                # last is zhai or 1, and now target decide to fei
                elif (last_guess[1] == 1 or last_guess[2]) and (target_guess_face != 1 and not target_guess_zhai):
                    target_decide[0] = 2 * last_guess[0] + target_guess_num
                else:
                    target_decide[0] = target_guess_num + last_guess[0]
                # Make an illegal start
                if not judge_legal_guess(last_guess, target_decide, len(player_list)):
                    if need_debug_info:
                        print('Target 做出了一个不合法的猜测')
                    target.GetReward(last_guess, target_decide, -99, learning_rate)
                    continue
                # Legal start for coachAI to decide open or not
                else:
                    coach_decide = coach.Decide(target_decide, greedy_epsilon)
                    while not judge_legal_guess(target_decide, coach_decide, len(player_list)):
                        coach_decide = coach.Decide(target_decide, greedy_epsilon + 0.1)

                    # Coach open target
                    if coach_decide[0] == 0:
                        if judge_open(target_decide, len(player_list), player_list, need_debug_info):
                            target.GetReward(last_guess, target_decide, -50, learning_rate)
                        else:
                            target.GetReward(last_guess, target_decide, 30, learning_rate)
                    # Coach continue
                    else:
                        target.GetReward(last_guess, target_decide, 20, learning_rate)
    # Just for Decide to generate the loss value
    target.Decide(last_guess, 0)
    # Build state vector to update
    state_vector = [last_guess[0], last_guess[1], bool(last_guess[2])]
    for dice_face in range(6):
        state_vector.append(player_list[0].dice_dict[dice_face])
    if isinstance(player_list[0], DQN_agent):
        player_list[0].Update(state_vector)

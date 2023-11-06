import random
import torch
import time
from GameAI import AI
from Qlearning import QlearningAIOneLevel
from DQN import DQN_agent, try_gpu
from utils import judge_legal_guess, judge_open

START_FACTOR = 0
ZHAI_FACTOR = 0.5
RANDOM_OPEN_FACTOR = 0.01

CONTINUE_REWARD = 20

BE_OPEN_REWARD = 10
BE_OPEN_PUNISH = -40

SUCCESSFUL_OPEN_REWARD = 70
UNSUCCESSFUL_OPEN_PUNISH = -50

ILLEGAL_PUNISH = -100


def output_train_info(target, epoch, last_output_time, last_output_epoch):
    if time.time() - last_output_time > 5:
        if isinstance(target, QlearningAIOneLevel):
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), 'epoch=', epoch,
                  '训练速度为', (epoch - last_output_epoch) / 5, 'epoch / s')
            target.zero_detect = 0
        if isinstance(target, DQN_agent):
            target.avg_loss = target.avg_loss / (target.update_time * target.length_of_guess_vector)
            target.decide_loss = target.decide_loss / target.decide_try
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), 'epoch=', epoch,
                  '训练速度为', (epoch - last_output_epoch) / 5, 'epoch / s',
                  'loss=', float(target.avg_loss),
                  '，平均决策误差为', target.decide_loss)
            target.update_time = 0
            target.decide_loss = 0.0
            target.decide_try = 0
            target.avg_loss = 0
        return True
    else:
        return False


def save_and_update_target(target, coach, num_player, last_save_time):
    if time.time() - last_save_time > 300:
        if isinstance(target, QlearningAIOneLevel):
            torch.save(target.Q_table, 'model/QlearningOneLevel/num' + str(num_player) + '.pt')
            print('已保存')
        if isinstance(target, DQN_agent):
            torch.save(target.net, 'model/DQN/DQN.pkl')
            print('已保存')
        if isinstance(coach, DQN_agent):
            coach.net = target.net
            print('已更新训练数据集')
        return True
    else:
        return False


def RandomTrain(targetAI, coachAI, learning_rate, greedy_epsilon, max_epoch, max_player_num, need_debug_info):
    target = targetAI(2, need_debug_info)
    coach = coachAI(2, need_debug_info)
    player_list = [target, coach]
    player_list[0].name = 'Target'
    player_list[1].name = 'Coach'
    last_output_time = time.time()
    last_save_time = time.time()
    last_output_epoch = 0
    if isinstance(player_list[0], DQN_agent):
        try:
            player_list[0].net = torch.load('model/DQN/DQN.pkl')
            player_list[0].net = player_list[0].net.to(device=try_gpu())
            if isinstance(player_list[1], DQN_agent):
                player_list[1].net = player_list[0].net
            print('成功读取 model/DQN/DQN.pkl')
        except FileNotFoundError:
            torch.save(player_list[0].net, 'model\\DQN\\DQN.pkl')
    print('正在开始训练，请稍后...')
    for epoch in range(max_epoch + 1):
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
                init_guess = [random.randint(player_num // 2, 3 * player_num), random.randint(2, 6), False]
                if need_debug_info:
                    print('Init 为', init_guess)
            else:
                # Init guess is Zhai
                init_guess = [random.randint(player_num // 2, 2 * player_num), random.randint(2, 6), True]
                if need_debug_info:
                    print('Init 为', init_guess)
            player_list[1].ShakeDice()
            epsilon = greedy_epsilon
            last_guess = player_list[1].Decide(init_guess, greedy_epsilon)
            while not judge_legal_guess(init_guess, last_guess, player_num):
                if need_debug_info:
                    print('last player 做出了一个不合法的猜测', last_guess)
                epsilon += 0.1
                last_guess = player_list[1].Decide(init_guess, epsilon)
            if last_guess[0] == 0:
                last_guess = [-1, 0, False]
                if need_debug_info:
                    print('last player 选择了开，强制将其设为', last_guess)
            if need_debug_info:
                print('last player 的点数为', player_list[1].dice)
            player_list[0].ShakeDice()
            Traverse_target_decide(player_list[0], player_list[1], player_list,
                                   last_guess, learning_rate, greedy_epsilon, need_debug_info)

        if output_train_info(player_list[0], epoch, last_output_time, last_output_epoch):
            last_output_time = time.time()
            last_output_epoch = epoch

        if save_and_update_target(player_list[0], player_list[1], player_num, last_save_time):
            last_save_time = time.time()


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
    # Just for Decide to generate the loss value
    target.Decide(last_guess, 0)
    for target_guess_num in range(4):
        # target decide to open
        if target_guess_num == 3:
            if last_guess[0] == -1:
                if need_debug_info:
                    print('Target 开了初始值!')
                    target_decide = [0, 0, False]
                    target.GetReward(last_guess, target_decide, ILLEGAL_PUNISH, learning_rate)
            else:
                if need_debug_info:
                    print('Target 选择开')
                target_decide = [0, 0, False]
                if judge_open(last_guess, len(player_list), player_list, need_debug_info):
                    target.GetReward(last_guess, target_decide, SUCCESSFUL_OPEN_REWARD, learning_rate)
                else:
                    target.GetReward(last_guess, target_decide, UNSUCCESSFUL_OPEN_PUNISH, learning_rate)
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
                    target.GetReward(last_guess, target_decide, ILLEGAL_PUNISH, learning_rate)
                    continue
                # Legal start for coachAI to decide open or not
                else:
                    random_open_factor = random.random()
                    if random_open_factor < RANDOM_OPEN_FACTOR:
                        if need_debug_info:
                            print('下家选择随机开！')
                        coach_decide = [0, 0, False]
                    else:
                        coach_decide = coach.Decide(target_decide, greedy_epsilon)
                        while not judge_legal_guess(target_decide, coach_decide, len(player_list)):
                            coach_decide = coach.Decide(target_decide, greedy_epsilon + 0.1)

                    # Coach open target
                    if coach_decide[0] == 0:
                        if judge_open(target_decide, len(player_list), player_list, need_debug_info):
                            if need_debug_info:
                                print('被开了且输了')
                            target.GetReward(last_guess, target_decide, BE_OPEN_PUNISH, learning_rate)
                        else:
                            if need_debug_info:
                                print('骗开成功')
                            target.GetReward(last_guess, target_decide, BE_OPEN_REWARD, learning_rate)
                    # Coach continue
                    else:
                        target.GetReward(last_guess, target_decide, CONTINUE_REWARD, learning_rate)

    # Build state vector to update
    state_vector = [last_guess[0], last_guess[1], bool(last_guess[2])]
    for dice_face in range(6):
        state_vector.append(player_list[0].dice_dict[dice_face])
    if isinstance(player_list[0], DQN_agent):
        player_list[0].Update(state_vector)

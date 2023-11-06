import random
import time
import numpy as np
import sys
sys.path.append('web')
sys.path.append('AI')
from web import libserver
import json
from AI.DQN import DQN_agent


class LiquorDiceGame:
    def __init__(self):
        self.dice_count = 5

    def roll_dice(self):  # 扔5个骰子，返回5个数的列表
        return [random.randint(1, 6) for _ in range(self.dice_count)]

    @staticmethod
    def choose_player(previous_guess, players):  # 选择玩家，第一回合随机选择玩家，其他回合按顺序选择玩家
        if previous_guess ==[]:  # 第一回合
            next_player_index = random.randint(0,len(players)-1)
        else:  # 其它回合
            last_player_index = players.index(previous_guess[-1][-1])  # 查找当前玩家在玩家表中的位置
            next_player_index = int((last_player_index + 1) % len(players))  # 顺序获得下一玩家的位置（计算下一玩家在玩家列表中的位置）
        return next_player_index

    @staticmethod
    def calculate_dices(all_dices):
        array_all_dices = np.array(all_dices)
        counts = [0, 0, 0, 0, 0, 0]  # 初始化记录骰子点数个数的列表
        for i in range(6):  # 记录各点数出现总次数
            counts[i] = np.count_nonzero(array_all_dices == i + 1)
        return counts

    @staticmethod
    def open_guess(previous_guess, counts, allow_zhai):  # 开玩家
        jump_num = 0  # 置0开上一个玩家
        be_opened_player_guess = previous_guess[-(jump_num + 1)]  # 导入被开玩家的猜测记录
        be_opened_player_rule = int(be_opened_player_guess[2])  # 被开玩家选择的rule
        guess_quantity = int(be_opened_player_guess[0])  # 猜测的数量
        guess_value = int(be_opened_player_guess[1])  # 猜测的数字
        if allow_zhai:  # 允许斋猜测
            # 判断开的结果
            if be_opened_player_rule == 0:  # 被开玩家选飞猜测
                if counts[guess_value - 1] + counts[0] >= guess_quantity:
                    results = False  # 当前玩家输，被开赢
                else:
                    results = True  # 当前玩家赢，被开输
            else:  # 被开玩家选斋猜测
                if counts[guess_value - 1] >= guess_quantity:
                    results = False  # 当前玩家输，被开赢
                else:
                    results = True  # 当前玩家赢，被开输
        else:  # 只有飞猜测
            if counts[guess_value - 1] + counts[0] >= guess_quantity:
                results = False  # 当前玩家输，被开赢
            else:
                results = True  # 当前玩家赢，被开输

        return results

    @staticmethod
    def make_guess(decide, previous_guess, current_player_name):
        guess = []
        guess.append(decide['num'])
        guess.append(decide['face'])
        guess.append(decide['zhai'])
        guess.append(current_player_name)  # str类型
        previous_guess.append(guess)  # 做出正确猜测后将该猜测存入列表

def main_game(
    player_name,
    player_read_fn,
    player_write_fn,
    max_player_num,  # 总玩家数量
    max_round,
    allow_zhai,
    allow_jump,
    player_socket):

    player_num = len(player_name)  # 真人玩家数
    ai_num = max_player_num - player_num  # ai玩家数量
    player_id = list(range(max_player_num))  # 玩家序号列表
    # 定义消息格式
    # 初始消息
    start_mesg = {
        'type': 'start_mesg',
        'total_num': max_player_num,  # 游戏总玩家数量
        'player_num': player_num,
        'ai_num': ai_num,  # ai数量
        'max_round': max_round,  # 游戏总轮数
        'current_round': 1,  # 当前游戏轮数
        'dice': [],  # 1*5的列表，一个玩家骰子结果
        'player_id': 1,
        'player_name': ''
    }
    # 服务器告知为某一玩家的回合
    Ask = {
        'type': 'Ask',
        'is_your_round': 1,
        'last_guess_num': 7,
        'last_guess_face':4,
        'last_guess_zhai':1

    }
    # 玩家继续猜测的输入
    decide = {
        'type': 'decide',
        'num': 7,  # 若为0则代表玩家选择开
        'face': 4,
        'zhai': 1
    }
    # 服务器广播某一玩家猜测的消息
    s2c_decide = {
        'type': 's2c_decide',
        'player_id': 1,
        'player_name': '',
        'num': 7,
        'face': 4,
        'zhai': 1
    }
    # 结束游戏的消息
    end = {
        'type': 'end',
        'dice': [],  # n*5的二维列表
        'name': [],  # 1*n的一维列表
        'info': ''  # 判决的打印信息
    }

    lq_game = LiquorDiceGame()  # 实例化一个游戏逻辑类
    ai_dict = {}  # 创建一个空字典来存储AI实例
    for i in range(ai_num):  # 实例化ai_num个ai并将其加入玩家名字列表
        ai_name = 'test_AI_' + str(i)
        player_name.append(ai_name)
        ai_dict[ai_name] = DQN_agent(max_player_num)  # 把AI实例存储到字典里
    # 游戏主循环
    for k in range(1, max_round+1):  # 10轮游戏
        # 广播初始消息
        end['dice'] = []
        time.sleep(5)
        for j in range(0, player_num):
            # 初始通信start的消息
            start_mesg['current_round'] = k  # 当前第几轮游戏
            start_mesg['dice'] = lq_game.roll_dice()  # 玩家骰子结果
            start_mesg['player_id'] = j  # 玩家序号
            start_mesg['player_name'] = player_name[j]  # 玩家名字
            start_mesg['total_num'] = max_player_num # 玩家数量

            # 服务器记录的骰子信息
            end['dice'].append(start_mesg['dice'])  # 把真人玩家骰子结果存储

            # 把初始消息发给真人玩家
            
            start_mesg_json = json.dumps(start_mesg)  # 将字典消息变为json字符串
            player_write_fn[j](start_mesg_json)
        # 服务器记录的骰子信息
        for j in range(0, ai_num):
            ai_name = 'test_AI_' + str(j)
            end['dice'].append(ai_dict[ai_name].dice.tolist())  # 把ai玩家骰子结果存储

        # 记录玩家的猜测
        previous_guess = []

        while True:
            time.sleep(5)
            # 选择玩家
            current_player_id = lq_game.choose_player(previous_guess, players=player_name)
            current_player_name = player_name[current_player_id]

            # 确定是否是ai玩家
            for i in range(1, ai_num+1):
                if current_player_id == player_id[-i]:  # 当前玩家id在最后ai_num位代表是ai玩家
                    if_is_AI = 1
                    break
                else:
                    if_is_AI = 0

            # ai玩家
            if if_is_AI == 1:
                ai_id = current_player_id-player_num
                ai_name = 'test_AI_' + str(ai_id)
                # 判断ai玩家是否是第一个玩家
                if previous_guess == []:
                    AI_guess = ai_dict[ai_name].Decide([-1, 1, 1])  # 列表第一个为-1告诉ai它是第一个玩家,返回[int,int,int]
                else:
                    last_guess = previous_guess[-1]  # [int,int,int,str]
                    last_guess.pop()  # [int,int,int]
                    AI_guess = ai_dict[ai_name].Decide(last_guess)  # 返回[int,int,int]

                # 判断玩家选择继续猜测还是选择开
                if_continue_guess = AI_guess[0]  # 不为0 代表继续猜测

                # 玩家选择继续猜测
                if if_continue_guess != 0:
                    AI_guess.append(current_player_name)  # 添加ai玩家名到列表
                    previous_guess.append(AI_guess)  # 存储猜测

                    # 发送的s2c_decide消息
                    s2c_decide['player_id'] = current_player_id
                    s2c_decide['player_name'] = current_player_name
                    s2c_decide['num'] = AI_guess[0]
                    s2c_decide['face'] = AI_guess[1]
                    s2c_decide['zhai'] = AI_guess[2]

                    # 广播发送该消息给真人玩家
                    
                    s2c_decide_json = json.dumps(s2c_decide)  # 将字典消息变为json字符串
                    for j in range(0, player_num):
                        player_write_fn[j](s2c_decide_json)
                # 玩家选择开
                else:
                    # 骰子结果
                    end['name'] = player_name  # 玩家名字顺序列表
                    counts = lq_game.calculate_dices(end['dice'])  # 返回一个记录着最终骰子结果的列表
                    results = lq_game.open_guess(previous_guess, counts, allow_zhai)  # 计算玩家是否开对了
                    last_player = previous_guess[-1][-1]  # 上一名玩家名字
                    if results:  # 当前玩家赢
                        end['info'] = f'玩家{current_player_name}开对了，赢得比赛！！！' \
                                      f'玩家{last_player}猜错了，输掉比赛！！！'
                    else:  # 当前玩家输
                        end['info'] = f'玩家{current_player_name}开错了，输掉比赛！！！' \
                                      f'玩家{last_player}猜对了，赢得比赛！！！'
                    # 在服务器端打印结果
                    print(end['info'])

                    # 广播消息给真人玩家
                    
                    end_json = json.dumps(end)  # 将字典消息变为json字符串
                    for j in range(0, player_num):
                        player_write_fn[j](end_json)
                    break

            # 真人玩家
            else:
                # 发送Ask消息
                if len(previous_guess) !=0:
                    Ask['last_guess_num'] = previous_guess[-1][0]
                    Ask['last_guess_face'] = previous_guess[-1][1]
                    Ask['last_guess_zhai'] = previous_guess[-1][2]
                else:
                    Ask['last_guess_num'] = -1
                    Ask['last_guess_face'] = -1
                    Ask['last_guess_zhai'] = -1
                
                
                # 用一个ask-decide建立连接
                
                Ask_json = json.dumps(Ask)  # 将字典消息变为json字符串
                player_write_fn[current_player_id](Ask_json)  # 告诉某玩家到他的回合
                # 等待玩家消息
                decide_json = player_read_fn[current_player_id]()  # 接收玩家消息
                decide = json.loads(decide_json)  # 使用json.loads()函数将JSON字符串转为字典
                print(decide)


                
                # 判断玩家选择继续猜测还是选择开
                if_continue_guess = decide['num']  # 不为0 代表继续猜测

                # 玩家选择继续猜测
                if if_continue_guess != 0:
                    lq_game.make_guess(decide, previous_guess, current_player_name)  # 存储猜测
                    # 发送的s2c_decide消息
                    s2c_decide['player_id'] = current_player_id
                    s2c_decide['player_name'] = current_player_name
                    s2c_decide['num'] = decide['num']
                    s2c_decide['face'] = decide['face']
                    s2c_decide['zhai'] = decide['zhai']

                    # 广播发送该消息
                    
                    s2c_decide_json = json.dumps(s2c_decide)  # 将字典消息变为json字符串
                    for j in range(0, player_num):
                        player_write_fn[j](s2c_decide_json)
                # 玩家选择开
                else:
                    # 骰子结果
                    end['name'] = player_name  # 玩家名字顺序列表
                    counts = lq_game.calculate_dices(end['dice'])  # 返回一个记录着最终骰子结果的列表
                    results = lq_game.open_guess(previous_guess, counts, allow_zhai)  # 计算玩家是否开对了
                    last_player = previous_guess[-1]  # 上一名玩家名字
                    if results:  # 当前玩家赢
                        end['info'] = f'玩家{current_player_name}开对了，赢得比赛！！！' \
                                      f'玩家{last_player}猜错了，输掉比赛！！！'
                    else:  # 当前玩家输
                        end['info'] = f'玩家{current_player_name}开错了，输掉比赛！！！' \
                                      f'玩家{last_player}猜对了，赢得比赛！！！'

                    # 在服务器端打印结果
                    print(end['info'])

                    # 广播消息
                    
                    end_json = json.dumps(end)  # 将字典消息变为json字符串
                    for j in range(0, player_num):
                        player_write_fn[j](end_json)
                    break

if __name__ == '__main__':
    libserver.start_server(main_game, '10.19.188.180', 12347)

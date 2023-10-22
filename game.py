import random
import numpy as np


class LiquorDiceGame:
    def __init__(self):
        self.dice_count = 5

    def roll_dice(self):  # 扔5个骰子，返回5个数的列表
        return [random.randint(1, 6) for _ in range(self.dice_count)]

    @staticmethod
    def choose_player(current_player, players):  # 选择玩家，第一回合随机选择玩家，其他回合按顺序选择玩家
        if current_player == None:  # 第一回合
            current_player = random.choice(players)
        else:  # 其它回合
            current_player_index = players.index(current_player)  # 查找当前玩家在玩家表中的位置
            next_player_index = int((current_player_index + 1) % len(players))  # 顺序获得下一玩家的位置（计算下一玩家在玩家列表中的位置）
            current_player = players[next_player_index]  # 更新当前玩家
        return current_player

    @staticmethod
    def calculate_dices(all_dices):
        array_all_dices = np.array(all_dices)
        counts = [0, 0, 0, 0, 0, 0]  # 初始化记录骰子点数个数的列表
        for i in range(6):  # 记录各点数出现总次数
            counts[i] = np.count_nonzero(array_all_dices == i + 1)
        return counts

    @staticmethod
    def open_guess(previous_guess, counts):  # 开玩家
        jump_num = 0  # 置0开上一个玩家
        be_opened_player_guess = previous_guess[-(jump_num + 1)]  # 导入被开玩家的猜测记录
        be_opened_player = be_opened_player_guess[3]  # 被开玩家名字
        be_opened_player_rule = int(be_opened_player_guess[2])  # 被开玩家选择的rule
        guess_quantity = int(be_opened_player_guess[0])  # 猜测的数量
        guess_value = int(be_opened_player_guess[1])  # 猜测的数字
        # 判断开的结果
        if be_opened_player_rule == 0:  # 被开玩家选飞猜测
            if counts[guess_value - 1] + counts[0] >= guess_quantity:
                results = False  # 当前玩家输
            else:
                results = True  # 当前玩家赢
        else:  # 被开玩家选斋猜测
            if counts[guess_value - 1] >= guess_quantity:
                results = False  # 当前玩家输
            else:
                results = True  # 当前玩家赢
        return results
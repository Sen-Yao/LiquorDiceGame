import random
import numpy as np


class LiquorDiceGame:
    def __init__(self, players):
        self.players = players
        self.dice_count = 5
        self.current_player = None
        self.previous_guess = []  # 记录过去所有玩家的猜测
        # previous_guess列表：[['7','4',True,'玩家1'],['7','5',False,'玩家2']]列表元素为有3个str值,1个bool值的列表，
        # 保存猜测的x个y，斋或飞猜测及给出猜测的玩家
        self.player_dice = self.roll_dice()  # 当前玩家的骰子结果
        self.all_dices = [self.player_dice]  # 所有玩家骰子结果汇总
        self.game_continue = True  # 游戏是否继续

    def roll_dice(self):  # 扔5个骰子，返回5个数的列表
        return [random.randint(1, 6) for _ in range(self.dice_count)]

    def choose_player(self):  # 选择玩家，第一回合随机选择玩家，其他回合按顺序选择玩家
        if self.current_player == None:  # 第一回合
            self.current_player = random.choice(self.players)
        else:  # 其它回合
            current_player_index = self.players.index(self.current_player)  # 查找当前玩家在玩家表中的位置
            next_player_index = int((current_player_index + 1) % len(self.players))  # 顺序获得下一玩家的位置（计算下一玩家在玩家列表中的位置）
            self.current_player = self.players[next_player_index]  # 更新当前玩家
        print(f'本轮游戏的玩家是:{self.current_player}!')

    def make_guess(self):
        guess = input("输入你的猜测，以空格分隔(例如:'7 4 0'),最后一个数字0代表飞猜测，1代表斋猜测：").split()
        # 检查输入的是否是两个数字
        if len(guess) != 3 or not guess[0].isdigit() or not guess[1].isdigit() or not guess[2].isdigit():
            print("你输入的不是数字或输入数字个数有误！请重新输入！")
            return self.make_guess()

        # 将猜测值转化为整数（先前按照str格式保存）,同时检查输入的数字是否有效
        guess_quantity = int(guess[0])
        guess_value = int(guess[1])
        guess_rule = int(guess[2])
        if guess_quantity < 1 or guess_value > 6 or guess_value < 1 or guess_rule < 0 or guess_rule > 1:
            print('输入的猜测非法！请重新输入猜测！')
            return self.make_guess()

        if self.previous_guess != []:  # 先前猜测不为空列表（本回合不是第一回合）
            last_guess = self.previous_guess[-1]  # 上一个玩家的猜测
            last_guess_quantity = int(last_guess[0])
            last_guess_value = int(last_guess[1])
            last_rule = int(last_guess[2])
            # 检查猜的值是否符合基本规则
            # 如果为飞猜测
            if guess_rule == 0:
                if last_rule == 0:  # 上局为飞猜测，本局为飞猜测
                    if guess_quantity <= last_guess_quantity and guess_value <= last_guess_value or guess_value == 1:
                        print("无效猜测！请输入正确的猜测 !")
                        return self.make_guess()
                if last_rule == 1:  # 上局为斋猜测，本局为飞猜测
                    if guess_quantity <= last_guess_quantity * 2 and guess_value <= last_guess_value or guess_value == 1:
                        print("无效猜测！请输入正确的猜测 !")
                        return self.make_guess()
            else:
                if last_rule == 0:  # 上局为飞猜测，本局为斋猜测
                    if guess_quantity <= int((last_guess_quantity + 1) / 2) and guess_value <= last_guess_value:
                        print("无效猜测！请输入正确的猜测 !")
                        return self.make_guess()
                if last_rule == 1:  # 上局为斋猜测，本局为斋猜测
                    if guess_quantity <= last_guess_quantity and guess_value <= last_guess_value:
                        print("无效猜测！请输入正确的猜测 !")
                        return self.make_guess()

        guess[2] = bool(guess_rule)  # 把1或0转化为bool值，false代表飞猜，true代表斋猜
        guess.append(self.current_player)  # 把玩家信息加入列表中，以便标识谁做出的猜测
        self.previous_guess.append(guess)  # 做出正确猜测后将该猜测存入列表

    def open_guess(self):
        num_players = len(self.players)  # 玩家人数
        if num_players >= 3:
            open_guess_mode = input('请选择你是否要跳开，跳开输入1，不跳开输入其他')
            if open_guess_mode == '1':
                jump_num = int(input('请指定你要跳开的玩家个数，例如：1（输入1代表你要跳上一个玩家去开上上个玩家）'))
            else:
                jump_num = 0
        else:
            jump_num = 0

        be_opened_player_guess = self.previous_guess[-(jump_num + 1)]  # 导入被开玩家的猜测记录
        be_opened_player = be_opened_player_guess[3]  # 被开玩家名字
        be_opened_player_rule = int(be_opened_player_guess[2])  # 被开玩家选择的rule
        print(f'玩家{self.current_player}选择开{be_opened_player}！')
        guess_quantity = int(be_opened_player_guess[0])  # 猜测的数量
        guess_value = int(be_opened_player_guess[1])  # 猜测的数字

        array_all_dices = np.array(self.all_dices)
        counts = [0, 0, 0, 0, 0, 0]  # 初始化记录骰子点数个数的列表
        for i in range(6):  # 记录各点数出现总次数
            counts[i] = np.count_nonzero(array_all_dices == i + 1)
        print(f'场上骰子各点数总个数如右:{counts}')

        if be_opened_player_rule == 0:  # 被开玩家选飞猜测
            if counts[guess_value - 1] + counts[0] >= guess_quantity:
                print(f'被开玩家猜测为真！当前玩家{self.current_player}输掉游戏！')
            else:
                print(f'被开玩家猜测为假！被开玩家{be_opened_player}输掉游戏！')
        else:  # 被开玩家选斋猜测
            if counts[guess_value - 1] >= guess_quantity:
                print(f'被开玩家猜测为真！当前玩家{self.current_player}输掉游戏！')
            else:
                print(f'被开玩家猜测为假！被开玩家{be_opened_player}输掉游戏！')

        print('请选择是否继续游戏！输入数字1继续游戏！否则结束游戏！')
        if_continue = input()
        if if_continue == '1':
            self.game_continue = False  # 选择开后游戏结束

    def choose_next_action(self):  # 选择继续猜测或是开
        print('选择你的行动：‘继续猜测’输入1,‘开’输入2！')
        action = input()
        if not action.isdigit():  # 输入的不是数字
            print('你输入的不是数字！请输入正确的数字来选择你的行动！')
            return self.choose_next_action()
        else:
            if action == '1':
                print('你选择继续猜测！')
                self.make_guess()
            elif action == '2':
                print('你选择开！')
                self.open_guess()
            else:
                print('无效输入！请输入正确的数字来选择你的行动！')
                return self.choose_next_action()

    def play_game(self):
        self.choose_player()  # 选择初始玩家开始游戏
        self.make_guess()  # 当前玩家做出猜测
        while True:
            self.choose_player()  # 选择下一位玩家
            self.choose_next_action()  # 该玩家选择“继续猜测”或“开”
            if not self.game_continue:
                break
        print('游戏结束！')


if __name__ == "__main__":
    players = ['玩家1', '玩家2', '玩家3', '玩家4', '玩家5', '玩家6', '玩家7']
    game = LiquorDiceGame(players)
    game.play_game()
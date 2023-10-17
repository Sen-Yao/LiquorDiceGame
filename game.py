import random
import numpy as np
import GUI
class LiquorDiceGame:

    def __init__(self, zhai_rule, jump_open_rule):
        """
        Initialize the class LiquorDiceGame
        """
        self.zhai_rule = zhai_rule
        self.jump_open_rule = jump_open_rule
        self.players = ['玩家1', '玩家2', '玩家3', '玩家4', '玩家5', '玩家6', '玩家7']
        self.dice_count = 5
        self.current_player = None
        self.last_rule = 1  # 记录上一次猜测为斋猜测还是飞猜测，记飞猜测为1，斋猜测为2
        self.previous_guess = []  # 记录玩家以往的猜测的列表
        # previous_guess列表：[['7','4','玩家1'],['7','5','玩家2']]列表元素为有三个str值的列表，保存猜测的x个y以及给出猜测的玩家

    def roll_dice(self,dice_count):  # 扔5个骰子，返回5个数的列表
        return [random.randint(1, 6) for _ in range(dice_count)]

    def choose_player(self, players, current_player):  # 选择玩家，第一回合随机选择玩家，其他回合按顺序选择玩家
        if current_player == None:  # 第一回合
            current_player = random.choice(players)
        else:  # 其它回合
            current_player_index = players.index(current_player)  # 查找当前玩家在玩家表中的位置
            next_player_index = int((current_player_index + 1) % len(players))  # 顺序获得下一玩家的位置（计算下一玩家在玩家列表中的位置）
            current_player = players[next_player_index]  # 更新当前玩家
        print(f'本轮游戏的玩家是:{current_player}!')
        return current_player

    def make_guess(self, current_player, previous_guess):
        guess = input("输入你的猜测，以空格分隔(例如:'7 4 1'),最后一个数字1代表飞猜测，2代表斋猜测：").split()
        global last_rule  # 记录上局是飞猜测还是斋猜测
        # 检查输入的是否是两个数字
        if len(guess) != 3 or not guess[0].isdigit() or not guess[1].isdigit() or not guess[2].isdigit():
            print("你输入的不是数字或输入数字个数有误！请重新输入！")
            return self.make_guess(current_player, previous_guess)

        # 将猜测值转化为整数（先前按照str格式保存）,同时检查输入的数字是否有效
        guess_quantity = int(guess[0])
        guess_value = int(guess[1])
        guess_rule = int(guess[2])
        if guess_quantity < 1 or guess_value > 6 or guess_value < 1 or guess_rule < 1 or guess_rule > 2:
            print('输入的猜测非法！请重新输入猜测！')
            return self.make_guess(current_player, previous_guess)

        if previous_guess != []:  # 先前猜测不为空列表（本回合不是第一回合）
            last_guess = previous_guess[-1]  # 上一个玩家的猜测
            last_guess_quantity = int(last_guess[0])
            last_guess_value = int(last_guess[1])
            # 检查猜的值是否符合基本规则
            # 如果为飞猜测
            if guess_rule == 1:
                if last_rule == 1:  # 上局为飞猜测，本局为飞猜测
                    if guess_quantity <= last_guess_quantity and guess_value <= last_guess_value or guess_value == 1:
                        print("无效猜测！请输入正确的猜测 !")
                        return self.make_guess(current_player, previous_guess)
                if last_rule == 2:  # 上局为斋猜测，本局为飞猜测
                    if guess_quantity <= last_guess_quantity * 2 and guess_value <= last_guess_value or guess_value == 1:
                        print("无效猜测！请输入正确的猜测 !")
                        return self.make_guess(current_player, previous_guess)
            else:
                if last_rule == 1:  # 上局为飞猜测，本局为斋猜测
                    if guess_quantity <= int((last_guess_quantity + 1) / 2) and guess_value <= last_guess_value:
                        print("无效猜测！请输入正确的猜测 !")
                        return self.make_guess(current_player, previous_guess)
                if last_rule == 2:  # 上局为斋猜测，本局为斋猜测
                    if guess_quantity <= last_guess_quantity and guess_value <= last_guess_value:
                        print("无效猜测！请输入正确的猜测 !")
                        return self.make_guess(current_player, previous_guess)

        guess.append(current_player)  # 把玩家信息加入列表中，以便标识谁做出的猜测
        previous_guess.append(guess)  # 做出正确猜测后将该猜测存入列表
        last_rule = guess_rule

    def open_guess(self, current_player, previous_guess, all_dices, num_players):
        if num_players >= 3:
            open_guess_mode = input('请选择你是否要跳开，跳开输入1，不跳开输入2')
            if open_guess_mode == 1:
                jump_num = int(input('请指定你要跳开的玩家个数，例如：1（输入1代表你要跳上一个玩家去开上上个玩家）'))
            else:
                jump_num = 0
        else:
            jump_num = 0
        beopened_player_guess = previous_guess[-(jump_num + 1)]  # 导入被开玩家的猜测记录
        beopened_player = beopened_player_guess[2]  # 上被开玩家名字
        print(f'玩家{current_player}选择开{beopened_player}！')
        guess_quantity = int(beopened_player_guess[0])  # 猜测的数量
        guess_value = int(beopened_player_guess[1])  # 猜测的数字

        array_all_dices = np.array(all_dices)
        counts = [0, 0, 0, 0, 0, 0]  # 初始化记录骰子点数个数的列表
        for i in range(6):  # 记录各点数出现总次数
            counts[i] = np.count_nonzero(array_all_dices == i + 1)
        print(f'场上骰子各点数总个数如右:{counts}')

        if last_rule == 1:  # 开的前一轮为飞猜测
            if counts[guess_value - 1] + counts[0] >= guess_quantity:
                print(f'被开玩家猜测为真！当前玩家{current_player}输掉游戏！')
            else:
                print(f'被开玩家猜测为假！被开玩家{beopened_player}输掉游戏！')
        else:  # 开的前一轮为斋猜测
            if counts[guess_value - 1] >= guess_quantity:
                print(f'被开玩家猜测为真！当前玩家{current_player}输掉游戏！')
            else:
                print(f'被开玩家猜测为假！被开玩家{beopened_player}输掉游戏！')

        global game_continue  # global该变量，修改以结束游戏
        game_continue = False

    def choose_next_action(self, num_players):  # 选择继续猜测或是开
        print('选择你的行动：‘继续猜测’输入1,‘开’输入2！')
        action = input()
        if not action.isdigit():  # 输入的不是数字
            print('你输入的不是数字！请输入正确的数字来选择你的行动！')
            return self.choose_next_action(num_players)
        else:
            if action == '1':
                print('你选择继续猜测！')
                self.make_guess(current_player, previous_guess)
            elif action == '2':
                print('你选择开！')
                self.open_guess(current_player, previous_guess, all_dices, num_players)
            else:
                print('无效输入！请输入正确的数字来选择你的行动！')
                return self.choose_next_action(num_players)

    pass

if __name__ == "__main__":
    # 初始化玩家和骰子数量
    players = ['玩家1', '玩家2', '玩家3', '玩家4', '玩家5', '玩家6', '玩家7']
    dice_count = 5
    current_player = None
    last_rule = 1 # 记录上一次猜测为斋猜测还是飞猜测，记飞猜测为1，斋猜测为2
    previous_guess = []  # 记录玩家以往的猜测的列表
    # previous_guess列表：[['7','4','玩家1'],['7','5','玩家2']]列表元素为有三个str值的列表，保存猜测的x个y以及给出猜测的玩家

    game = LiquorDiceGame()

    # 玩家初始掷骰子
    player_dice = game.roll_dice(dice_count)
    num_players = len(players)

    # 获得所有玩家骰子信息
    all_dices = []  # 存储所有玩家的骰子结果
    all_dices.append(player_dice)  # 这里应该是进行通信获得其他玩家骰子信息
    # print(all_dices)  # 测试用

    # 选择初始玩家开始游戏
    current_player = game.choose_player(players, current_player)

    # 当前玩家做出猜测
    game.make_guess(current_player, previous_guess)

    game_continue = True
    while game_continue:
        # 选择下一位玩家
        current_player = game.choose_player(players, current_player)
        # 该玩家选择“继续猜测”或“开”
        game.choose_next_action(num_players)

    print('游戏结束！')
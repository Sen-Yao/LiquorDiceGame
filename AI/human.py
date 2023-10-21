from GameAI import AI


class Human(AI):
    """
    A dump AI, base on traditional algorithm to generate a response.
    """

    def __init__(self, num_player, need_output=False):
        """
        Initialize the base information
        """
        super().__init__(num_player, need_output)
        self.name = '人类'

    def ShowDice(self):
        if self.need_output or isinstance(self, Human):
            print(self.name, '玩家的骰子结果为', self.dice)

    def Decide(self, input_list, ge):
        """
        The AI will react depends on its dices result only
        :return: An action list
        """
        while True:
            if input_list[0] == 0:
                print('上一个玩家喊开！')
            elif input_list[2]:
                print('上一个玩家喊出了', input_list[0], '个', input_list[1], '斋')
            else:
                print('上一个玩家喊出了', input_list[0], '个', input_list[1])
            self.guess[0] = int(input('第一个数字'))
            if self.guess[0] == 0:
                print(self.name, '玩家选择主动开！')
                yield [0, 0, False, self.name]
            self.guess[1] = int(input('第二个数字'))
            self.guess[2] = bool(int(input('斋飞')))
            self.guess[3] = self.name
            if bool(self.guess[2]):
                print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1], '斋')
            else:
                print(self.name, '玩家喊出', self.guess[0], '个', self.guess[1])
            print('\n')
            yield self.guess

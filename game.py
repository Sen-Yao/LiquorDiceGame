class LiquorDiceGame:

    def __init__(self, zhai_rule, jump_open_rule):
        """
        Initialize the class LiquorDiceGame
        """
        self.game_pointer = None  # Which player is in action
        self.num_decks = None
        self.num_players = None

        # num_actions means how many action can a player take
        # A Guess
        self.num_actions = None
        self.zhai_rule = zhai_rule
        self.jump_open_rule = jump_open_rule

    def configure(self, game_config):
        """ Specify some game specific parameters, such as number of players
        """
        self.num_players = game_config['game_num_players']
        self.num_decks = game_config['game_num_decks']

    def get_num_players(self):
        """ Return the number of players in blackjack

        Returns:
            number_of_player (int): blackjack only have 1 player
        """
        return self.num_players

    def get_num_actions(self):
        """ Return the number of applicable actions

        Returns:
            number_of_actions (int): there are only two actions (open and stand)
        """
        return self.num_actions

    def get_player_id(self):
        """ Return the current player's id

        Returns:
            player_id (int): current player's id
        """
        return self.game_pointer
    
    def init_game(self):
        """ Initialize the game

        Returns:
            state (dict): the first state of the game
            player_id (int): current player's id
        """

    def step(self, action):
        """ Get the next state

        Args:
            action (str): a specific action of Liquor Dice Game. (Open or Guess)

        Returns:/
            dict: next player's state
            int: next player's id
        """
    def is_over(self):
        """ Check if the game is over

        Returns:
            status (bool): True/False
        """

    def a(self):
        print('a')
        pass

    pass

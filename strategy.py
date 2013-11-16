class BetStrategy():
    """
    Defines a strategy for a poker game via the method analyze_gamestate,
    which modifies instance variables of this class to reflect the recommended
    bet for the current GameState (passed to analyze_gamestate)
    """	       
    def __init__(self, accuracy=100):
		self.recommended_bet = -1
		self.accuracy = accuracy
    
    def analyze_gamestate(self, gamestate):
		"""
		Modifies the current state of self.recommended_bet, depending on
		the GameState that is passed in.  If a bet is recommended,
		recommended_bet will be set to some positive value, anything <= 0
		is a recommendation to checkfold.
		@param gamestate: The current table layout.
		@type gamestate: a Gamestate object.
		"""
		probability = self._find_probability_of_win(self.accuracy, gamestate)
		value = gamestate.pot
		expected_value = probability * value
		self.recommended_bet = expected_value

		
    def _find_probability_of_win(self, number_of_games, gamestate):
		"""
		Takes a GameState object and simulates the provided number of games
		with it, then divides the player wins by the total and returns that
		result.

        @param number_of_games: The number of games to be simulated
		@type number_of_games: an int object.
		@param gamestate: The game to be simulated.
		@type gamestate: a Gamestate object.
		"""
		wins = 0
		for x in range(0, number_of_games):
			wins += gamestate.simulate_game()
		return float(wins) / number_of_games
	

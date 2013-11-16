"""
gamestate.py
contains all the information essential to a poker game table at any moment.
"""
from handrank import *

class GameState:
    """
    Gamestate stores all the information necessary for any
    round of holdem.  This inclues, the players pocket cards,
    the number of opponents, the visible board cards, the size
    of the pot and the minimum bet.
    
    Gamestate also provides methods to randomly extrapolate the
    game to its conclusion, i.e. draw random cards to fill out
    the rest of the board and the opponents hands.
    """
    def __init__(self, pcards, opponents, board, pot, minbet):
		self.pcards = pcards
		self.opponents = opponents
		self.board = board
		self.pot = pot
		self.minbet = minbet
		self.opcards = []
		self.reset_deck()

    def update_hands(self):
		"""
		Takes the cards given and creates hands for the player and
		each opponents (composed of the hole cards stored in
		player_cards and opponents_cards plus the board cards stored
		in board)
		"""
		self.phand = Hand(self.pcards + self.board)
		self.ophands = []
		for cards in self.opcards:
			h = Hand(cards)
			h.cards += self.board
			self.ophands.append(h)

    def reset_deck(self):
        """
        Replaces Gamestate.deck with a new Deck()
        """
        self.deck = Deck()
        for card in (self.pcards + self.board):
            self.deck.cards.remove(card)

    def extrapolate_board(self):
        """
        Randomly draws cards from the deck and appends them
        to the board cards given in the init call, until all 
        five board cards have been selected
        """
        self.old_board = []
        self.old_board.extend(self.board)
        while len(self.board) < 5:
            self.board.append(self.deck.draw())

    def reset_board(self):
        """
        Returns Gamestate.board to its original self (spec. in
        the init call), and puts the cards that were added back
        into the deck.  old_board is then reset to an empty list. 
        """
        for card in self.board:
            if card not in self.old_board:
                self.deck.cards.append(card)
                self.board.remove(card)
        self.old_board = []

    def extrapolate_opponents(self):
		"""
		Takes the number of opponents given in self.opponents and draws two random cards for each of them, storing the results list in self.opcards.
		"""
		while len(self.opcards) < self.opponents:
			cards = [self.deck.draw()]
			cards.append(self.deck.draw())
			self.opcards.append(cards)

    def reset_opponents(self):
        """
        Returns self.opcards to empty and returns the cards
        selected for it to the deck.
        """
        for cards in self.opcards:
            for card in cards:
                self.deck.cards.append(card)
        self.opcards = []

    def extrapolate_game(self):
        """
        Extrapolates opponents and board.
        See Gamestate.extrapolate_opponents and
        Gamestate.extraoplate_board
        """
        self.extrapolate_opponents()
        self.extrapolate_board()

    def reset_game(self):
        """
        Resets opcards, board and the deck to their 
        original state.
        """
        self.reset_opponents()
        self.reset_board()

    def simulate_game(self):
		"""
		Extrapolates a game (Gamestate.extrapolate_game), then
		checks to see if the winner is the player's hand, resets
		the game (Gamestate.reset_game) and returns a 1 if the
		player won and a zero otherwise.
		"""
		self.extrapolate_game()
		self.update_hands()
		winner = max(self.ophands + [self.phand])
		self.reset_game()
		self.update_hands()
		if winner == self.phand:
			return 1
		else:
			return 0
        

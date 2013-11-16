from random import randrange, shuffle

class Card:
    """
    Stores a rank and a suit, and defines printing
    and comparison behavior.  Cards are ranked by their
    rank only, suit makes no effect.
    
    Suits must be in [0,1,2,3], defined as [clubs, hearts,
    spades, diamonds] respectively.
    """

    def __init__(self, *args):
		if len(args) == 1:
			suits = {"c": 0, "h": 1, "s": 2, "d": 3}
			self.rank = int(args[0][:-1])
			self.suit = int(suits[args[0][-1:]])
		elif len(args) == 2:
			self.rank = int(args[0])
			self.suit = int(args[1])
		else:
			raise Exception, "Either give rank and suit as seperate args or a single string"
		if self.rank not in range(-1,13):
			raise Exception, "Rank must be in range [-1,12] inclusive."
		if self.suit not in range(0,4):
			raise Exception, "Suit must be in range [0,3] inclusive."
		
    def __str__(self):
        return "[" + str(self.rank) + ", " + str(self.suit) + "]"

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return cmp(self.rank, other.rank)


class Deck:
    """
    A collection of cards, initialized to contain a full
    standard deck, 52 cards, with 13 of each suit, 4 of each
    rank, by convention.  
    """
    def __init__(self):
        self.cards = []
        for suit in range(0,4):
            for rank in range(0,13):
                self.cards.append(Card(rank, suit))

    def __str__(self):
        return ",".join([str(card) for card in self.cards])

    def __repr__(self):
        return "Deck with " + str(len(self.cards)) + " left."

    def draw(self, numcards=1):
        """
        Randomly removes a card from self.cards and returns it.
        """
        return self.cards.pop(randrange(0,len(self.cards)))
    
    def draw_with_rank(self, rank):
        """
        Removes a random card with the given rank.
        """
        def rankcond(card):
            if card.rank == rank: return True
            else: return False
        return self.draw_with_cond(rankcond)
    
    def draw_with_ranksuit(self, rank, suit):
        """
        Removes the card specified by the given rank and suit.
        """
        def rscond(card):
            if card.suit == suit and card.rank == rank:
                return True
            else: return False
        return self.draw_with_cond(rscond)
    
    def draw_with_cond(self, cond):
        """
        Takes a function that returns either true or false
        and uses it to choose a random card from the deck that
        passes that condition.

        Raises a TypeError if cond is not a function.
        """
        try:
            card = None
            shuffle(self.cards)
            for card in self.cards:
                if cond(card):
                    self.cards.remove(card)
                    return card
            return None
        except TypeError:
            print "Error: condition passed to Deck.draw_with_cond \
            is not a function."
            
    
class Hand:
    """
	Stores a list of cards and attributes for a rank (a number 0-9) and kickers, a list of cards representing the kickers for this hand. If not specified, rank and kickers are initialized to -1 and [] by default, until this Hand is assigned values for them (either directly or through a hand test function.)
    """
    def __init__(self, cards, rank=-1, kickers=[]):
        for card in cards:
            if card.__class__ != Card:
                raise Exception, "param cards must be a list of Cards"
        self.cards = cards
        self.rank = rank
        self.kickers = kickers
        self.reset_test_stack()
        
    def __str__(self):
        ret = "[Hand: {"
        for card in self.cards:
            ret += str(card) + ", "
        ret += "}"
        ret += "Rank = " + str(self.rank)
        ret += "Kickers = " + str(self.kickers) + "]"
        return ret

    def __repr__(self):
        ret = "[Hand: len(cards) = "
        ret += str(len(self.cards))
        ret += ", rank = "
        ret += str(self.rank)
        ret += ", kickers = " + str(self.kickers) + "]"
        return ret
    
    def countranks(self):
        """
        Returns a list of ints, with the indexes of that list
        representing the ranks and the values representing
        the number of times that rank occurs in this hand.
        """
        counts = []
        while len(counts) < 13: counts.append(0)
        for card in self.cards:
            counts[card.rank] += 1
        return counts
        
    def countcardswith(self, attr, value):
        """
        Takes a string either rank or suit and a value
        and returns the number of times a Card with that
        value in that attribute (via a call to getattr)
        occurs in Hand.cards
        
        Can cause an AttributeError if attr is not a member
        of Card.
        """
        count = 0
        for card in self.cards:
            try:
                if getattr(card, attr) == value:
                    count += 1
            except AttributeError:
                print "wrong attr string for countcards"

    def isranked(self):
        """
        Returns a 0 if self.rank has been assigned a value >= 0.
        1, otherwise.
        """
        if self.rank >= 0: return 1
        else: return 0

    def __cmp__(self, other):
		"""
		Hand comparison will only run as many tests as needed
		to determine which hand has a higher rank.  If ranks
		are equal, kickers are compared by ascending index.
		"""
		try:
			if self.isranked() and other.isranked():
				return self.cmp_ranked(other)
			elif self.isranked() or other.isranked():
				return self.cmp_ranked_unranked(other)
			else:
				return self.cmp_unranked(other)
		except AttributeError:
			print "comparing hand to something not hand"
            
    def cmp_unranked(self, other):
		"""
		Helper function for hand.__cmp__, takes two hands
		which are not ranked and runs their tests until
		a ranking is found for one of them.  Since tests
		are done in reverse rank order, as soon as one test
		gets a rank and the other doesn't, the final cmp
		value gets returned (1, or -1).  If both hands have
		the same rank, the return is a call to hand.__cmp__
		(which will then call Hand.cmp_ranked)
		"""
		if len(self.test_stack) != len(other.test_stack):
			if len(self.test_stack) > len(other.test_stack):
				moretestshand = self
			else:
				moretestshand = other
			while len(self.test_stack) != len(other.test_stack):
				(passed, rank, kickers) = moretestshand.run_next_test()
				if passed:
					moretestshand.rank = rank
					moretestshand.kickers = kickers
					if moretesthand is self: return 1
					else: return -1
		while len(self.test_stack) > 0:
			(selfpass, srank, skickers) = self.run_next_test()
			(otherpass, orank, okickers) = other.run_next_test()
			if selfpass:
				self.rank = srank
				self.kickers = skickers
				if not otherpass: return 1
			if otherpass:
				other.rank = orank
				other.kickers = okickers
				if not selfpass: return -1
			if selfpass and otherpass:
				return self.cmp_ranked(other)
                
    def cmp_ranked_unranked(self, other):
        """
        Compares one ranked hand and one unranked hand by
        applying tests to the unranked hand until it either
        finds a rank for it (and returns the ranked comparison)
        or it exhausts the tests for a rank higher than the ranked
        hand, in which case the ranked hand must be greater so it
        returns 1.
        """
        if self.isranked():
            unranked = other
            ranked = self
        else:
            unranked = self
            ranked = other
        while len(unranked.test_stack) > ranked.rank:
            (passed, rank, kickers) = unranked.run_next_test()
            if passed:
                unranked.rank = rank
                unranked.kickers = kickers
                return self.cmp_ranked(other) 
        if self is ranked: return 1
        else: return -1

    def run_next_test(self):
        """
        Takes the next test function off the stack and returns it.
        (see Hand.reset_test_stack)
        """
        return self.test_stack.pop()(self)

    def reset_test_stack(self):
        """
        Creates a new HandTest() object and stores its alltests_inorder
        attribute locally.
        """
        self.test_stack = HandTests().alltests_inorder
        self.test_stack.reverse()

    def cmp_ranked(self, other):
        """
        Takes two hands whose ranks have been initialized and
        returns the comparison of those ranks.  If they are equal,
        kickers are compared in order.
        
        Can raise an IndexError if the kickers of a Hand are 
        incorrectly defined, that is, two Hands of the same rank
        have an unequal number of kickers.
        """
        if self.rank != other.rank:
            return cmp(self.rank, other.rank)
        try:
            for k in range(0, len(self.kickers)):
                unequal =  cmp(self.kickers[k], other.kickers[k])
                if unequal: return unequal
            return 0
        except IndexError:
            print "2 hands with same rank have unequal len(kickers)."
            
            
            
class HandTests:
    """
    A collection of tests to run on hands to determine their
    rank (and kickers).
    
    Has only one data attribute: alltests_inorder, a list of 
    member functions in order of descending rank (associated
    with the hand rank they are testing.)
    
    Each function takes an instance of Hand, and returns a 
    3-tuple consiting of:
    - An int, 0 or 1 depending on whether the hand passed the test,
    - An int, the rank of the hand that was found.
    - A list of Cards, the kickers for that hand.
    If the hand passes the test, the rank and kickers in the return
    reflect the newfound rank.  Otherwise the originals are returned
    unchanged.
    """

    def __init__(self):
        self.sffound = None
        self.alltests_inorder = [self.rsftest, self.sftest, 
                                 self.quadstest, self.boattest,
                                 self.flushtest, self.straighttest,
                                 self.tripstest, self.twopairtest,
                                 self.pairtest, self.highcard]

    def flushtest(self, hand):
        """
        Determines if the hand param has a flush.
        (See HandTest.__doc__ for more details.)
        """
        suitcounts = [0, 0, 0, 0]
        for card in hand.cards:
            suitcounts[card.suit] += 1
        for suit in range(0,4):
            if suitcounts[suit] >= 5:
                rank = 5
                flushcards = [card for card in hand.cards 
                                if card.suit == suit]
                kickers = flushcards
                kickers.sort(); kickers.reverse()
                kickers = kickers[:5]
                return 1, rank, kickers
        return 0, hand.rank, hand.kickers
    
    def straighttest(self, hand):
        """(or cards if numcards is given),
        
        Determines if the hand param has a straight.
        (See HandTest.__doc__ for more details.)
        """
        cards = hand.cards[:]
        cards.sort()
        cards.reverse()
        prevrank = cards[0].rank
        acefound = 0
        straightcards = [cards[0]]
        for index in range(1, len(cards)):
            currentrank = cards[index].rank
            if currentrank == 12: acefound = 1
            if (prevrank - currentrank == 1 or 
                (currentrank == 0 and acefound)):
                straightcards.append(cards[index])
                if len(straightcards) == 5: break
            elif prevrank - currentrank > 1:
                straightcards = [cards[index]]    
            prevrank = currentrank
        if len(straightcards) == 5:
            rank = 4
            kickers = straightcards
            if kickers[1].rank == 0:
                kickers = straightcards[1:] + [Card(-1, straightcards[0].suit)]
            return 1, rank, kickers
        else:
            return 0, hand.rank, hand.kickers
        
    def rsftest(self, hand, royal=1): 
        """
        Determines if the hand param has a straight flush.
        (See HandTest.__doc__ for more details.)
        """
        (passed, rank, kickers) = self.flushtest(hand)
        if passed:
            flushsuit = kickers[0].suit
            cards = [c for c in hand.cards if c.suit == flushsuit]
            (spassed, srank, skickers) = self.straighttest(Hand(cards))
            if spassed:
                if not royal:
                    return 1, 8, skickers
                else:
                    self.sffound = 1, 8, skickers 
                if skickers[0].rank == 12:
                    return 1, 9, skickers
        return 0, hand.rank, hand.kickers
    
    def sftest(self, hand):
        if self.sffound != None: return self.sffound
        if len(hand.test_stack) == 10:
            return self.rsftest(hand, royal=0)
        return 0, hand.rank, hand.kickers
    
    def boattest(self, hand): 
        """
        Determines if the hand param has a full house/boat.
        (See HandTest.__doc__ for more details.)
        """    
        return self.sequencetest(hand, [2, 3], 6)
        
    def quadstest(self, hand): 
        """
        Determines if the hand param has four of a kind.
        (See HandTest.__doc__ for more details.)
        """
        return self.sequencetest(hand, [4], 7)
    
    def tripstest(self, hand): 
        """
        Determines if the hand param has three of a kind.
        (See HandTest.__doc__ for more details.)
        """
        return self.sequencetest(hand, [3], 3)
    
    def twopairtest(self, hand): 
        """
        Determines if the hand param has two pair.
        (See HandTest.__doc__ for more details.)
        """
        return self.sequencetest(hand, [2, 2], 2)
    
    def pairtest(self, hand): 
        """
        Determines if the hand param has a pair.
        (See HandTest.__doc__ for more details.)
        """        
        return self.sequencetest(hand, [2], 1)
        
    def highcard(self, hand): 
        """
        Returns the rank and kickers for the highest
        cards in order for the hand.
        (See HandTest.__doc__ for more details.)
        """        
        kickers = hand.cards[:]
        kickers.sort()
        kickers.reverse()
        return 1, 0, kickers[:5]
    
    
    def sequencetest(self, hand, sizes, handrank):
        """
        Tests if the hand contains the sequences specified
        in the params. sizes is a list of ints, each one 
        representing the length of a sequence.  So,
        sizes = [3] tests for three-kind, sizes = [2,3]
        tests for a boat, etc.
        handrank is the rank that goes to a hand that
        fulfills the sequence specs.
        """
        # the reverse ordering of sizes here is so that
        # we test the long sequences first, which are far
        # more likely to fail (and we return early).
        sizes.sort()
        sizes.reverse()
        cards = hand.cards[:]
        counts = Hand(cards).countranks()
        kickers = []
        for size in sizes:
            maxrank = -1
            for rank, count in zip(range(13), counts):
                if (count >= size and 
                (rank not in [card.rank for card in kickers])):
                    maxrank = rank
            if maxrank >= 0: 
                for card in cards[:]:
                    if card.rank == maxrank:
                        kickers.append(card)
                        cards.remove(card)
            else: return 0, hand.rank, hand.kickers
        while len(kickers) < 5: kickers.append(max(cards))
        return 1, handrank, kickers[:5]
                    
            
        
            

import random
from handrank import *
from random import shuffle

__doc__ = \
"""
Contains functions that generate random hands of 
a certain type, e.g. a random flush or a random
hand that isn't a straight, and so forth.

Every function is called without args and returns
a single Hand instance.  Hand.rank and Hand.kickers
are not specified, so these hands are unranked.
"""

def generate_random_flush():
        """
        Creates a flush Hand at random, with
        rank and kicker left to default (i.e. unranked)
        """
        deck = Deck()
        cards = []
        flushsuit = randrange(0,4)
        for x in range(0,6):
            card = Card(randrange(0,13), flushsuit)
            while deck.cards.count(card) == 0:
                card = Card(randrange(0,13), flushsuit)
            deck.cards.remove(card)
            cards.append(card)
        for x in range(0,2):
            cards.append(deck.draw())
        return Hand(cards)

def generate_notflush():
    """
    Generates a hand that is guaranteed not to contain
    a flush.
    """
    deck = Deck()
    suitcounts = [0,0,0,0]
    cards = []
    while len(cards) < 7:
        card = deck.draw()
        while suitcounts[card.suit] == 4:
            card = deck.draw()
        cards.append(card)
        suitcounts[card.suit] += 1
    return Hand(cards)

def generate_random_straight(withflush=None, withrank=None):
    """
    Generates a random hand that is guaranteed to contain a 
    straight, by default.  The two optional params, withflush
    and withrank allow the caller to specify that the straight 
    cards must all have the suit withflush or the rank withrank.
    (i.e. for royal-straight-flush or straight-flush)
    """
    deck = Deck()
    if withrank != None:
        startingrank = withrank
    else:
        startingrank = randrange(0,9)
    cards = []
    for k in range(0,5):
        rank = startingrank + k
        if rank > 12 and len(cards) == 1:   
            rank -= 13
        if withflush != None:
            cards.append(deck.draw_with_ranksuit(rank, withflush))
        else:
            cards.append(deck.draw_with_rank(rank))    
    cards.append(deck.draw())
    cards.append(deck.draw())
    shuffle(cards)
    return Hand(cards)

def generate_notstraight():
    """
    Returns a random hand that is guaranteed not to
    contain a straight.
    """
    deck = Deck()
    cards = []
    rank = randrange(0,13)
    for k in range(0, 7):
        rank += 2
        if rank > 12: 
            rank -= 13    
        cards.append(deck.draw_with_rank(rank))
    return Hand(cards)

def generate_random_rsf():
    """
    Returns a random hand that is guaranteed to contain a 
    royal straight flush.
    """
    suit = randrange(0,4)
    rank = 8
    return generate_random_straight(withflush=suit, withrank=rank)
            
def generate_random_sf():
    """
    Returns a random hand that is guaranteed to contain a
    straight flush.
    """
    suit = randrange(0,4)
    return generate_random_straight(withflush=suit)

def generate_random_pair():
    """
    Returns a random hand that is guaranteed to contains the 
    number of pairs specified in the parameter, which is 1
    by default.
    """
    return generate_random_ranksets()

def generate_random_twopair():
    """
    Returns a random hand that is guaranteed to contains the 
    number of pairs specified in the parameter, which is 1
    by default.
    """
    return generate_random_ranksets([2,2])

def generate_random_ranksets(sequence=[2]):
    """
    Returns a random hand that is guaranteed to contain the 
    given number of sets with the specified length.  That is,
    for the param of the form [a, b, c...] a, b, c ints and 
    n = list length, this function will return a hand that 
    contains a number of cards with one rank, b with another rank
    and so forth, for a total of n sequences.
    
    When called without params, will return a pair.
    """
    if sum(sequence) > 7:
        raise Exception, ("Hand.generate_random_ranksets:, \
                        sequence param calling for more than \
                        seven cards. sum(sequence) = " + str(sum(sequence)))
    cards = []
    deck = Deck()
    ranks = range(13)
    for size in sequence:
        rank = ranks.pop(randrange(len(ranks)))
        for k in range(size):
            card = deck.draw_with_rank(rank)
            cards.append(card)
    while len(cards) < 7:
        def test(card):
            if card.rank in ranks: return 1
            else: return 0
        cards.append(deck.draw_with_cond(test))
    return Hand(cards)

def generate_random_boat():
    """
    Returns a random hand that is guaranteed to contains a
    full house / boat.
    """
    seq = random.choice([[3, 2, 1, 1], [3, 2, 2], [3, 3, 1]])
    random.shuffle(seq)
    return generate_random_ranksets(seq)
    
def generate_random_quads():
    """
    Returns a random hand that is guaranteed to contains a
    four of a kind.
    """
    return generate_random_ranksets([4])

def generate_random_trips():
    """
    Returns a random hand that is guaranteed to contain a
    three of a kind.
    """
    return generate_random_ranksets([3])

def generate_notrsf():
    """
    Returns a random hand that is guaranteed to not contain
    a royal straight flush.
    """
    hand1 = generate_notsf()
    hand2 = generate_random_sf()
    hands = [hand1, hand2]
    for card in hand2.cards:
        if card.rank == 12:
            hands = [hand1]
    return random.choice(hands)
    
def generate_notsf():
    """
    Returns a random hand that is guaranteed to not contain
    a straight flush.
    """
    hand1 = generate_notstraight()
    hand2 = generate_notflush()
    return random.choice([hand1, hand2])

def generate_notboat():
    """
    Returns a random hand that is guaranteed not to contain
    full house / boat (though it may contain any higher rank)
    """
    seq = random.choice([[1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 2],
            [1, 1, 1, 2, 2],
            [1, 2, 2, 2],
            [1, 1, 1, 1, 3]])
    random.shuffle(seq)
    return generate_random_ranksets(seq)
    

def generate_notquads():
    """
    Returns a random hand that is guaranteed not to contain
    four of a kind (though it may contain any higher rank)
    """
    seq = random.choice([[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 2],
                        [1, 1, 1, 2, 2],
                        [1, 2, 2, 2],
                        [1, 1, 1, 1, 3],
                        [1, 3, 3],
                        [1, 1, 2, 3],
                        [2, 2, 3]])
    random.shuffle(seq)
    return generate_random_ranksets(seq)
    
def generate_nottrips():
    """
    Returns a random hand that is guaranteed not to contain
    three of a kind (though it may contain any higher rank)
    """
    seq = random.choice([[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 2],
                        [1, 1, 1, 2, 2],
                        [1, 2, 2, 2]])
    random.shuffle(seq)
    return generate_random_ranksets(seq)
    
def generate_nottwopair():
    """
    Returns a random hand that is guaranteed not to contain
    two pairs (though it may contain any higher rank)
    """
    seq = random.choice([[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 2]])
    random.shuffle(seq)
    return generate_random_ranksets(seq)

def generate_notpair():
    """
    Returns a random hand that is guaranteed not to contain
    a pair (though it may contain any higher rank)
    """
    return generate_random_ranksets([1,1,1,1,1,1,1])

def generate_random_highcard():
    return generate_notpair()



def generate_only(rank):
    """
    Generates a hand that will only pass the given test
    and those below it in rank.  So for boattest, it must
    not pass fourkindtest, sftest or rsftest.  The generator
    provided must eventually create a hand that will fulfill
    these criteria or this function will not finish.
    """
    alltests = HandTests().alltests_inorder
    alltests.reverse()
    test = alltests[rank]
    tests = alltests[rank + 1:]
    gen = _allgens[rank]
    print "test = ", test
    print "gen = ", gen
    print "rank = ", rank
    while True:
        hand = gen()
        if len(tests) == 0: return hand
        for tfunc in tests:
            if tfunc(hand)[0]:
                break
        else:
            return hand
    
_allgens = (generate_random_highcard, generate_random_pair,
             generate_random_twopair, generate_random_trips,
             generate_random_straight, generate_random_flush,
             generate_random_boat, generate_random_quads,
             generate_random_sf, generate_random_rsf)

    
def allgens_inorder():
    return (generate_random_highcard, generate_random_pair,
             generate_random_twopair, generate_random_trips,
             generate_random_straight, generate_random_flush,
             generate_random_boat, generate_random_quads,
             generate_random_sf, generate_random_rsf)

def allonlygens_inorder():
    onlygens = []
    tests = HandTests().alltests_inorder
    tests.reverse()
    for gen, test, rank in zip(allgens_inorder(), tests, range(10)):
        def onlygen():
            return generate_only(test, gen, rank)
        onlygens.append(onlygen)
    return onlygens














import unittest
from handrank import *
from random import randrange, shuffle
from handgen import *


class HandTestFunctions:
    """
    Stores functions needed to test a particular handranking function.
    (see HandRankingTest.test_rankingtest)
    """
    def __init__(self, testfunc, passgen, failgen, resulttest):
        self.testfunc = testfunc
        self.passgen = passgen
        self.failgen = failgen
        self.resulttest = resulttest
    
    
class HandRankingTest(unittest.TestCase):
    """
    Contains test functions for all the hand ranking test
    functions contained in deck.HandTests.
    
    Setup builds a series of HandTestFunctions objects, each
    one containing functions necessary to test the hand with
    test_rankingtest().  All functions with name test. followed
    by a hand rank (e.g. flush, straight, pair, etc.) are designed
    to check the rank and kickers results from a HandTests function
    to ensure they are correct.
    """    
    
    def setUp(self):
        self.iterations = 30 #Number of times each test repeats for new inputs
        self.testfuncs = []
        self.testfuncs.append(HandTestFunctions(HandTests().flushtest, 
                                            generate_random_flush,
                                            generate_notflush,
                                            self.test_flushtest))
        self.testfuncs.append(HandTestFunctions(HandTests().straighttest, 
                                            generate_random_straight,
                                            generate_notstraight,
                                            self.test_straighttest))
        self.testfuncs.append(HandTestFunctions(HandTests().boattest, 
                                            generate_random_boat,
                                            generate_notboat,
                                            self.test_boattest))
        self.testfuncs.append(HandTestFunctions(HandTests().quadstest, 
                                            generate_random_quads,
                                            generate_notquads,
                                            self.test_quadstest))
        self.testfuncs.append(HandTestFunctions(HandTests().tripstest, 
                                            generate_random_trips,
                                            generate_nottrips,
                                            self.test_tripstest))
        self.testfuncs.append(HandTestFunctions(HandTests().twopairtest, 
                                            generate_random_twopair,
                                            generate_nottwopair,
                                            self.test_twopairtest))
        self.testfuncs.append(HandTestFunctions(HandTests().pairtest, 
                                            generate_random_pair,
                                            generate_notpair,
                                            self.test_pairtest))
        self.testfuncs.append(HandTestFunctions(HandTests().rsftest, 
                                            generate_random_rsf,
                                            generate_notrsf,
                                            self.test_rsftest))
        self.testfuncs.append(HandTestFunctions(HandTests().sftest, 
                                            generate_random_sf,
                                            generate_notsf,
                                            self.test_sftest))
                
        
    def test_main(self):
        for testfunc in self.testfuncs:
            self.test_rankingtest(testfunc)

    def test_flushtest(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 5
        for card in kickers1:
            for othercard in kickers1:
                assert card.suit == othercard.suit

    def test_straighttest(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 4
        prevcard = kickers1[0]
        for k in range(1,len(kickers1)):
            card = kickers1[k]
            assert prevcard.rank - card.rank == 1
            prevcard = card
    
    def test_boattest(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 6
        cards = []
        kickers1.reverse()
        while len(cards) < 3: cards.append(kickers1.pop())
        assert cards[0].rank == cards[1].rank == cards[2].rank
        cards = []
        while len(cards) < 2: cards.append(kickers1.pop())
        assert cards[0].rank == cards[1].rank
    
    def test_rsftest(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 9
        ranks = range(8, 13)
        ranks.reverse()
        for rank, card in zip(ranks, kickers1):
            assert rank == card.rank
        
    def test_sftest(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 8
        self.test_flushtest(passhand, nopasshand, 5, 
                      kickers1, rank2, kickers2)
        self.test_straighttest(passhand, nopasshand, 4, 
                      kickers1, rank2, kickers2)
        
    def test_tripstest(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 3
        assert kickers1[0].rank == kickers1[1].rank == kickers1[2].rank
        
    def test_quadstest(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 7
        assert (kickers1[0].rank == kickers1[1].rank == 
        kickers1[2].rank == kickers1[3].rank)
        
    def test_twopairtest(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 2
        assert kickers1[0].rank == kickers1[1].rank
        assert kickers1[2].rank == kickers1[3].rank
        assert kickers1[0].rank > kickers1[2].rank
    
    def test_pairtest(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 1
        assert kickers1[0].rank == kickers1[1].rank
        
    def test_highcard(self, passhand, nopasshand, rank1, 
                      kickers1, rank2, kickers2):
        assert rank1 == 0
        for k in range(0,4):
            assert kickers1[k].rank - kickers1[k+1].rank == 1
            
    def test_rankingtest(self, testfunctions):
        """
        Repeats a loop for the specified number of iterations, wherein
        it creates two hands: one from a call to passgenerator and the
        other to nopassgenerator.  These hands are then passed through
        test, and the rank and len(kickers) are checked according to the
        params.  Moretests is a functions that contains additional tests
        to be run, it must take the same params as test_rankingtest but
        without itself of course.
        """
        for x in range(0, self.iterations):
            passhand = testfunctions.passgen()
            nopasshand = testfunctions.failgen()
            (pass1, rank1, kickers1) = testfunctions.testfunc(passhand)
            (pass2, rank2, kickers2) = testfunctions.testfunc(nopasshand)
            assert pass1 == 1
            assert pass2 == 0
            assert rank2 == -1
            assert len(kickers1) == 5
            assert len(kickers2) == 0
            testfunctions.resulttest(passhand, nopasshand, rank1, kickers1, 
                                     rank2, kickers2)

class HandCompareTest(unittest.TestCase):
    """
    Tests for the cmp functionality in Hand.
    """
    def setUp(self):
        self.tests = HandTests().alltests_inorder
        self.tests.reverse()
        #self.gens = allonlygens_inorder()
        self.precision = 30
    
    def test_main(self):
        self.test_unequal_unranked()
        self.test_unequal_oneranked()
        self.test_unequal_ranked()
        self.test_equalhands(ranked=0)
        self.test_equalhands(ranked=1)
        self.test_equalhands(ranked=2)
#        
    def test_unequal_unranked(self):
        """ Tests a hand compare between two hands, both
        unranked.  One hand will yield a higher rank than
        the other by design (see only gens in handgen).
        """
        for x in range(self.precision):
            winnerrank = randrange(1,10)
            loserrank = randrange(0,winnerrank)
            print "wr = ", winnerrank
            print "lr = ", loserrank
            winner = generate_only(winnerrank)
            loser = generate_only(loserrank)
            print winner
            print loser
            print winner > loser
            assert winner > loser
            assert not (winner <= loser)
    
    def test_unequal_oneranked(self):
        """ Tests a hand compare between two hands, both
        unranked.  One hand will be ranked, and the other
        will be unranked.  The hands are unequal rank by
        design.
        """
        for x in range(self.precision):
            winnerrank = randrange(1,10)
            loserrank = randrange(0,winnerrank)
            winner = generate_only(winnerrank)
            loser = generate_only(loserrank)
            whandrank = winner, winnerrank
            lhandrank = loser, loserrank
            randhand, rhrank = random.choice([whandrank, lhandrank])
            result = self.tests[rhrank](randhand)
            randhand.rank = result[1]
            randhand.kickers = result[2]
            assert result[0] #This just tests the test functions not cmp
            assert winner > loser
            assert not (winner <= loser)
    
    def test_unequal_ranked(self):
        """ Tests a hand compare between two hands, both
        ranked.  The compare should not yield true for
        ==, by design.
        """
        for x in range(self.precision):
            winnerrank = randrange(1,10)
            loserrank = randrange(0,winnerrank)
            winner = generate_only(winnerrank)
            loser = generate_only(loserrank)
            (p, winner.rank, winner.kickers) = self.tests[winnerrank](winner)
            (q, loser.rank, loser.kickers) = self.tests[loserrank](loser)
            assert p and q #This just tests the test functions not cmp
            assert winner > loser
            assert not (winner <= loser)
            
    def test_equalhands(self, ranked=0):
        """ Tests hand compare for two hands that are
        equal rank by designed.  The optional param ranked
        controls how many of the 2 hands will be ranked prior
        to testing Hand.cmp.  By default, ranked is 0 and 
        so the function will rank both hands.  1 ranks only
        one hand chosen at random and 2 ranks neither.
        """
        for x in range(self.precision):
            rank = randrange(0,10)
            h1 = generate_only(rank)
            h2 = generate_only(rank)
            if ranked == 2:
                (p, h1.rank, h1.kickers) = self.tests[rank](h1)
                (q, h2.rank, h2.kickers) = self.tests[rank](h2)
                assert p and q #This just tests the test functions not cmp
                assert len(h1.kickers) == len(h2.kickers)
            elif ranked == 1:
                (p, h1.rank, h1.kickers) = self.tests[rank](h1)
                assert p #This just tests the test functions not cmp
            cmpresult = cmp(h1, h2)
            for k1, k2 in zip(h1.kickers, h2.kickers):
                if k1.rank > k2.rank:
                    assert cmpresult == 1
                    break
                elif k2.rank > k1.rank:
                    assert cmpresult == -1
                    break
            else:
                assert h1 == h2
    
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
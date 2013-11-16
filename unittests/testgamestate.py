"""
Tests for gamestate.py
"""
from gamestate import *

pranks = [1,8]
psuits = [2,2]
board = [Card(0,1), Card(0,2), Card(0,3)]
pcards = [Card(rank, suit) for rank, suit in zip(pranks, psuits)]

gs = Gamestate(pcards, 4, board, 5, 0.25)
gs.update_hands()

print "after gs.upd:"
print gs.phand
print gs.ophands

gs.extrapolate_board()

print "after extrapolate_board:"
print board

gs.update_hands()

print "after new update:"
print gs.phand
print gs.ophands

gs.reset_game

for x in range(0,4):
    print "Run #", x, ":"
    print gs.simulate_game()
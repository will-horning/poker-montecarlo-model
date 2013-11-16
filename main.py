from gamestate import GameState
from strategy import *
from handrank import *
import sys

args = sys.argv[1:]
pcards = [Card(args[0]), Card(args[1])]
opponents = int(args[2])
board = [Card(arg) for arg in args[3:-2]]
pot = float(args[-2])
minbet = float(args[-1])
gs = GameState(pcards, opponents, board, pot, minbet)
strat = BetStrategy(accuracy=1000)
strat.analyze_gamestate(gs)
print "EV = " + str(strat.recommended_bet)




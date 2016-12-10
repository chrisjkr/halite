from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("krszwsk v1")

def move(location):
    site = gameMap.getSite(location)
    if site.strength <  site.production * 5:
        return Move(location, STILL)
    return Move(location, NORTH if random.random() > 0.5 else WEST)

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    sendFrame(moves)

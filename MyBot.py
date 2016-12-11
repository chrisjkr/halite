from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("krszwsk v5")

def findClosestEdge(location):
    lowest_distance = min(gameMap.width / 2, gameMap.height / 2)
    lowest_coordinate = NORTH
    if location.x < gameMap.width / 2 and location.x < lowest_distance:
        lowest_distance = location.x
        lowest_coordinate = WEST
    if location.x > gameMap.width / 2 and gameMap.width - location.x < lowest_distance:
        lowest_distance = gameMap.width - location.x
        lowest_coordinate = EAST
    if location.y < gameMap.height / 2 and location.y < lowest_distance:
        lowest_distance = location.y
        lowest_coordinate = SOUTH
    if location.y > gameMap.height / 2 and gameMap.height - location.y < lowest_distance:
        lowest_distance = gameMap.height - location.y
        lowest_coordinate = NORTH
    return Move(location, lowest_coordinate)

def move(location):
    site = gameMap.getSite(location)
    border = False
    # Check every neighbour site
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if neighbour_site.owner != myID: 
            border = True # Site is a border
            # Attack if stronger
            if site.strength > neighbour_site.strength:
                return Move(location, d)
    # If site has enemy neighbour and has less strength, just wait
    if border or site.strength < site.production * 5:
        return Move(location, STILL)
    return findClosestEdge(location)

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    sendFrame(moves)

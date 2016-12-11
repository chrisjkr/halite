from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("krszwsk v6")

def findClosestBorder(location):
    max_distance = min(gameMap.width / 2, gameMap.height / 2)
    direction = NORTH
    for d in CARDINALS:
        distance = 0
        current = location
        site = gameMap.getSite(current, d)
        while site.owner == myID and distance < max_distance:
            distance += 1
            current = gameMap.getLocation(current, d)
            site = gameMap.getSite(current)
        if distance < max_distance:
            direction = d
            max_distance = distance
    return direction

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
    return Move(location, findClosestBorder(location))

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    sendFrame(moves)

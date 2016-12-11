from hlt import *
from networking import *
import logging as l

l.basicConfig(filename='MyBot.log', level=l.DEBUG)
l.disabled = True

myID, gameMap = getInit()
sendInit("krszwsk v6")

def dirToStr(d):
    if d == STILL:
        return 'STILL'
    elif d == NORTH:
        return 'NORTH'
    elif d == EAST:
        return 'EAST'
    elif d == SOUTH:
        return 'SOUTH'
    elif d == WEST:
        return 'WEST'

def findClosestBorder(location):
    l.info('findClosestBorder called width location ' + str(location.x) + ', ' + str(location.y) + '.')
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
        l.info('Distance to border in ' + dirToStr(d) + ' direction is ' + str(distance))
        if distance < max_distance:
            direction = d
            max_distance = distance
    l.info('Closest border is ' + dirToStr(direction) + ' with distance ' + str(distance))
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

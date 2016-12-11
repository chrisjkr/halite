import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging as l

l.basicConfig(filename='v2.log', level=l.DEBUG)
l.disabled = False

myID, game_map = hlt.get_init()
hlt.send_init("krszwsk v2")

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

def find_closest_border(square):
    l.info('findClosestBorder called width location ' + str(square.x) + ', ' + str(square.y) + '.')
    max_distance = min(game_map.width / 2, game_map.height / 2)
    direction = NORTH
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square
        while current.owner == myID and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, d)
        l.info('Distance to border in ' + dirToStr(d) + ' direction is ' + str(distance))
        if distance < max_distance:
            direction = d
            max_distance = distance
    l.info('Closest border is ' + dirToStr(direction) + ' with distance ' + str(distance))
    return direction

def move(square):
    border = False
    # Check if there's a weaker enemy neighbour
    for d, neighbour in enumerate(game_map.neighbours(square)):
        # Check if neighbour is enemy
        if neighbour.owner != myID:
            border = True
            # Fight if enemy is weaker
            if neighbour.strength < square.strength:
                return Move(square, d)

    if border or square.strength < square.production * 5:
        return Move(square, STILL)

    return Move(square, find_closest_border(square))

while True:
    game_map.get_frame()
    moves = [move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)

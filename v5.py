import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging as l
import time

l.basicConfig(filename='v5.log', level=l.DEBUG)
l.disabled = True

myID, game_map = hlt.get_init()
hlt.send_init("krszwsk v5")

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

def get_nice_string(list_or_iterator):
    return "[" + ", ".join( str(x) for x in list_or_iterator) + "]"

def find_closest_border(square):
    max_distance = min(game_map.width / 2, game_map.height / 2)
    direction = NORTH
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square
        while current.owner == myID and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, d)
        if distance < max_distance:
            direction = d
            max_distance = distance
    return direction

def find_path_to_location(home, target):
    if home.x == target.x and home.y == target.y:
        return STILL
    if abs(home.x - target.x) >= abs(home.y - target.y):
        if home.x > target.x:
            return WEST
        else:
            return EAST
    else:
        if home.y > target.y:
            return NORTH
        else:
            return SOUTH

def move(square):
    border = False

    # Check if there's a weaker enemy neighbour
    weakest_neighbour_strength = 255
    for d, neighbour in enumerate(game_map.neighbours(square)):
        # Check if neighbour is enemy
        if neighbour.owner != myID:
            border = True
            # Fight if enemy is weaker
            if neighbour.strength < square.strength:
                return Move(square, d)
            else:
                if neighbour.strength < weakest_neighbour_strength:
                    weakest_neighbour_strength = neighbour.strength

    if square.strength > square.production * 5:
        for weakest in come_here:
            if game_map.get_distance(square, weakest[0]) < 2 and weakest[1] < weakest_neighbour_strength:
                return Move(square, find_path_to_location(square, weakest[0]))

    come_here.append([square, weakest_neighbour_strength])

    if border or square.strength < square.production * 4:
        return Move(square, STILL)

    return Move(square, find_closest_border(square))

while True:
    game_map.get_frame()
    start = time.time()
    come_here = []
    moves = []
    for square in game_map:
        if time.time() - start > 1.2:
            break
        if square.owner == myID:
            moves.append(move(square))
    hlt.send_frame(moves)

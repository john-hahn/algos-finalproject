# CS272 Final Project
# Suhaas, Steven, John

import sys
import numpy as np

GRID_SIZE = 400
TIME = 1440

class Attraction:
    def __init__(self, x, y, open, close, util, duration):
        self.x = x
        self.y = y
        self.open = open
        self.close = close
        self.util = util
        self.duration = duration
    

def greedy():
    return


def read_input():
    N = int(input())
    attractions = []
    for i in range(N):
        x, y, open, close, util, duration = [int(i) for i in input().split()]
        a1 = Attraction(x, y, open, close, util, duration)
        attractions.append(a1)
    return N, attractions


def main():
    N, attractions = read_input()
    optimal_route = greedy(N, attractions)
    print(optimal_route)


if __name__ == '__main__':
    main()
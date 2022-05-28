# CS272 Final Project
# Suhaas, Steven, John

from importlib.resources import path
import math
import os
import sys
from tracemalloc import start
import numpy as np

GRID_SIZE = 400
TIME = 1440


# receive input
#   create array of attractions
#   get number of nodes in the attraction
#   call our solve function

# greedy
#   declare start_node
#   declare path variable (to_implement)
#   declare time_left variable
#   while time available
#       run lowest_cost fxn and append the val to path,
#       remove that attraction from attractions array
#       subtract that time taken from time left
#   return path

# lowest_cost(attraction_from, attractions)
#   declare min: infinity
#   for each in attraction
#       calculate cost
#       if cost < min: min = cost
#   return min_attraction

class Attraction:
    def __init__(self, id, x, y, open, close, util, duration):
        self.id = id
        self.x = x
        self.y = y
        self.open = open
        self.close = close
        self.util = util
        self.duration = duration

    def __repr__(self):
        return "Attraction %s: x: %s, y: %s, open: %s, close: %s, util: %s, duration: %s" % (self.id, self.x, self.y, self.open, self.close, self.util, self.duration)

    def travel_time(self, end):
        return math.sqrt((self.x - end.x)**2 + (self.y - end.y)**2)

    def is_closed(self, end, curr_time, start_to_end):
        time_reach = curr_time + start_to_end
        return end.open > time_reach or end.close < time_reach

    def can_reach_home(self, end, curr_time, start_to_end):
        tot_time = curr_time + \
            start_to_end + end.duration + \
            math.sqrt((end.x - 200)**2 + (end.y - 200)**2)
        return tot_time <= TIME

    def is_viable(self, end, curr_time):
        start_to_end = self.travel_time(end)
        if not self.can_reach_home(end, curr_time, start_to_end) or self.is_closed(end, curr_time, start_to_end):
            return False
        return True

    def cost(self, end):
        dist = self.travel_time(end)
        time = end.duration
        util = end.util
        if util == 0:
            return math.inf
        return (dist**2) * (time**1.4) / (util**3)


def greedy(attractions):

    tot_util = 0

    number_of_attractions = 0
    attractions_visited = []
    curr_time = 0

    start_node = Attraction(-1, 200, 200, -1, -1, -1, -1)
    current_node = start_node

    while curr_time < TIME:
        lowest_node = None
        lowest_cost = math.inf
        for attraction in attractions:
            if current_node.is_viable(attraction, curr_time):
                prospective_cost = current_node.cost(attraction)
                if prospective_cost < lowest_cost:
                    lowest_cost = prospective_cost
                    lowest_node = attraction

        if lowest_node is None:
            return number_of_attractions, attractions_visited

        number_of_attractions += 1

        attractions_visited.append(lowest_node.id)
        attractions.remove(lowest_node)

        curr_time += lowest_node.duration + \
            current_node.travel_time(lowest_node)
        current_node = lowest_node
        tot_util += current_node.util
    return number_of_attractions, attractions_visited


def read_input(file):
    N = int(file.readline())
    attractions = []
    for i in range(N):
        x, y, open, close, util, duration = [
            int(i) for i in file.readline().split()]
        a1 = Attraction(i+1, x, y, open, close, util, duration)
        attractions.append(a1)
    return N, attractions

# SAMPLE INPUT
# 3
# x-coord y-coord open-time close-time util duration
# 50 100 0 1440 50 100
# 100 100 20 50 1000 50


def main():
    for file in os.listdir('all_inputs'):
        if file.endswith('.in'):
            basename = os.path.basename(file)[:-3]
            f = open("all_inputs/" + file, 'r')
            N, attractions = read_input(f)
            optimal_route = greedy(attractions)
            print(optimal_route)
            optimal_route = (optimal_route[0], ' '.join(
                str(v) for v in optimal_route[1]))
            write_file = open('all_outputs/' + basename + '.out', 'w')
            write_file.write('\n'.join(str(v) for v in optimal_route))


if __name__ == '__main__':
    main()

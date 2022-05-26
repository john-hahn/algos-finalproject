# CS272 Final Project
# Suhaas, Steven, John

from importlib.resources import path
import math

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

    def is_viable(self, end, curr_time):
        tot_time = curr_time + \
            self.travel_time(end) + end.duration + \
            math.sqrt((end.x - 200)**2 + (end.y - 200)**2)
        if tot_time > TIME:
            return False
        return True

    def cost(self, end):
        dist = self.travel_time(end)
        time = end.duration
        util = end.util
        return dist * time / util


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

        # testing purposes
        for i in attractions:
            print(i.id)

        attractions_visited.append(lowest_node.id)
        attractions.remove(lowest_node)

        curr_time += lowest_node.duration + \
            current_node.travel_time(lowest_node)
        current_node = lowest_node
        tot_util += current_node.util
        print(tot_util)
    return number_of_attractions, attractions_visited


def read_input():
    N = int(input())
    attractions = []
    for i in range(N):
        x, y, open, close, util, duration = [int(i) for i in input().split()]
        a1 = Attraction(i, x, y, open, close, util, duration)
        attractions.append(a1)
    return N, attractions

# SAMPLE INPUT
# 3
# x-coord y-coord open-time close-time util duration
# 50 100 0 1440 50 100
# 100 100 20 50 1000 50
#


def main():
    N, attractions = read_input()
    optimal_route = greedy(attractions)
    print(optimal_route)


if __name__ == '__main__':
    main()

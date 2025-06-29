from queue import PriorityQueue
from .state import *
from itertools import count

def heuristic(car):
    return abs(car.coord[1] - 4)

def a_star(start):
    frontier = PriorityQueue()
    unique = count()
    dist = {}
    result = None

    frontier.put((heuristic(start.cars[0]), next(unique), start))
    while not frontier.empty():
        cost, _, current = frontier.get()
        if current.cars[0].coord[1] + current.cars[0].length == 6:
            path = []
            while current != start:
                path.append(current)
                current = current.parent
            path.append(start)
            path.reverse()
            return path

        current_tuple = current.to_tuple()
        if current_tuple in dist and dist[current_tuple] < cost: # Skip longer path
            continue

        for state in current.next_states():
            new_cost = heuristic(state.cars[0]) + state.cost
            state_tuple = state.to_tuple()
            if state_tuple not in dist or new_cost < dist[state_tuple]:
                dist[state_tuple] = new_cost
                frontier.put((new_cost, next(unique), state))

    return None

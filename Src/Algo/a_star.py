from queue import PriorityQueue
from .state import *
from itertools import count

def heuristic(car, m):
    car_x = car.coord[1]
    start_x = car_x + car.length
    num_block_cars = 0
    for i in range(start_x, 6):
        if m[car.coord[0]][i]:
            num_block_cars += 1
    return abs(car.coord[1] - 4) + num_block_cars

def a_star(start):
    frontier = PriorityQueue()
    unique = count()
    explored = set()
    dist = {} # for faster frontier lookup
    state_count = 0

    frontier.put((heuristic(start.cars[0], start.generate_map()), next(unique), start))
    dist[start.to_tuple()] = 0
    while not frontier.empty():
        state_count += 1
        _, _, current = frontier.get()
        cur_tup = current.to_tuple()
        dist.pop(cur_tup)

        if current.cars[0].coord[1] + current.cars[0].length == 6:
            path = []
            while current != start:
                path.append(current)
                current = current.parent
            path.append(start)
            path.reverse()
            print(f"Expanded nodes: {state_count}")
            return path

        explored.add(cur_tup)
        for state in current.next_states():
            new_cost = heuristic(state.cars[0], state.generate_map()) + state.cost
            state_tuple = state.to_tuple()
            # If child node not in explored and not in frontier
            if state_tuple not in explored and state_tuple not in dist:
                dist[state_tuple] = new_cost
                frontier.put((new_cost, next(unique), state))

    return None

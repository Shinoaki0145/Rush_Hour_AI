import heapq
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
    frontier = []
    unique = count()
    explored = set()
    state_count = 0

    heapq.heappush(frontier, (heuristic(start.cars[0], start.generate_map()), next(unique), start))
    while frontier:
        state_count += 1
        _, _, current = heapq.heappop(frontier)

        if current.cars[0].coord[1] + current.cars[0].length == 6:
            path = []
            while current != start:
                path.append(current)
                current = current.parent
            path.append(start)
            path.reverse()
            print(f"Expanded nodes: {state_count}")
            return path

        explored.add(current.to_tuple())
        for state in current.next_states():
            new_cost = heuristic(state.cars[0], state.generate_map()) + state.cost
            state_tuple = state.to_tuple()
            if (state_tuple not in explored and
                not any(s.to_tuple() == state_tuple for _,_,s in frontier)):
                heapq.heappush(frontier, (new_cost, next(unique), state))

    return None

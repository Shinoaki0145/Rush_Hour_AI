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
    state_count = 0
    frontier = []
    unique = count()
    explored = set()

    start_heuristic = heuristic(start.cars[0], start.generate_map())
    heapq.heappush(frontier, (start_heuristic, next(unique), start))
    dist = {start.to_tuple() : start_heuristic}
    while frontier:
        cost, _, current_state = heapq.heappop(frontier)
        cur_tup = current_state.to_tuple()
        if cur_tup in dist and cost > dist[cur_tup]:
            continue
        dist.pop(cur_tup, None)
        state_count += 1
        
        target_car = current_state.cars[0]
        if not target_car.vertical and target_car.coord[1] + target_car.length == 6:
            path = []
            while current_state != start:
                path.append(current_state)
                current_state = current_state.parent
            path.append(start)
            path.reverse()
            return path, state_count

        explored.add(cur_tup)
        for next_state in current_state.next_states():
            state_tuple = next_state.to_tuple()
            if state_tuple in explored:
                continue

            new_cost = heuristic(next_state.cars[0], next_state.generate_map()) + next_state.cost
            if state_tuple not in dist or new_cost < dist[state_tuple]:
                dist[state_tuple] = new_cost
                heapq.heappush(frontier, (new_cost, next(unique), next_state))

    return None, state_count

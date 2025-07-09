import heapq
from itertools import count
from .state import *

def ucs(start_state):
    state_count = 0
    frontier = []
    explored = set()
    unique = count() 

    heapq.heappush(frontier, (start_state.cost, next(unique), start_state))
    dist = {start_state.to_tuple() : start_state.cost}
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
            while current_state != start_state:
                path.append(current_state)
                current_state = current_state.parent
            path.append(start_state)
            path.reverse()
            return path, state_count

        explored.add(cur_tup)
        for next_state in current_state.next_states():
            state_tuple = next_state.to_tuple()
            if (state_tuple not in explored 
                and (state_tuple not in dist or next_state.cost < dist[state_tuple])):
                dist[state_tuple] = next_state.cost
                heapq.heappush(frontier, (next_state.cost, next(unique), next_state))

    return None, state_count

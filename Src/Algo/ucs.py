import heapq
from itertools import count
from .state import *

def ucs(start_state):
    frontier = []
    unique = count() 

    heapq.heappush(frontier, (start_state.cost, next(unique), start_state))
    explored = set()
    
    state_count = 0
    while frontier:
        state_count += 1
        _, _, current_state = heapq.heappop(frontier)

        # Kiểm tra goal
        main_car = current_state.cars[0]
        if not main_car.vertical and main_car.coord[1] + main_car.length == 6:
            # Truy vết đường đi
            path = []
            while current_state != start_state:
                path.append(current_state)
                current_state = current_state.parent
            path.append(start_state)
            path.reverse()
            print(f"Expanded nodes: {state_count}")
            return path

        explored.add(current_state.to_tuple())

        for next_state in current_state.next_states():
            state_tuple = next_state.to_tuple()
            if (state_tuple not in explored and
                not any(s.to_tuple() == state_tuple for _,_,s in frontier)):
                heapq.heappush(frontier, (next_state.cost, next(unique), next_state))

    return None  # Không tìm thấy lời giải

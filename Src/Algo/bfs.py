from collections import deque
from .state import *

def bfs(start):
    state_count = 0
    if start.cars[0].coord[1] + start.cars[0].length == 6:
        print(f"Expanded nodes: {state_count}")
        return [start]
    
    frontier = deque()
    explored = set()

    frontier.append(start)
    fast_frontier = {start.to_tuple()}
    while frontier:
        state_count += 1
        current_state = frontier.popleft() 
        cur_tup = current_state.to_tuple()
        fast_frontier.remove(cur_tup)
        explored.add(cur_tup)
        
        for next_state in current_state.next_states():
            state_tuple = next_state.to_tuple()
            
            if (state_tuple not in explored and state_tuple not in fast_frontier):
                target_car = next_state.cars[0]
                if not target_car.vertical and target_car.coord[1] + target_car.length == 6:
                    # Truy vết đường đi
                    path = []
                    while next_state != start:
                        path.append(next_state)
                        next_state = next_state.parent
                    path.append(start)
                    path.reverse()
                    print(f"Expanded nodes: {state_count}")
                    return path
                 
                fast_frontier.add(state_tuple)
                frontier.append(next_state)

    return None
from collections import deque
from .state import *

def bfs(start):
    frontier = deque()
    frontier.append(start)
    explored = set()
    state_count = 0

    while frontier:
        state_count += 1
        current_state = frontier.popleft() 

        explored.add(current_state.to_tuple())

        for next_state in current_state.next_states():
            state_tuple = next_state.to_tuple()
            # Không nằm trong explored và frontier
            if (state_tuple not in explored and
               not any(s.to_tuple() == state_tuple for s in frontier)):
                #  Kiểm tra goal: xe 0 đi ngang, ra tới cột 5
                if next_state.cars[0].coord[1] + next_state.cars[0].length == 6:
                    # Truy vết đường đi
                    path = []
                    while next_state != start:
                        path.append(next_state)
                        next_state = next_state.parent
                    path.append(start)
                    path.reverse()
                    print(f"Expanded nodes: {state_count}")
                    return path 
                frontier.append(next_state)

    return None  # Không tìm thấy lời giải
from collections import deque
from .state import *

def bfs(start):
    frontier = deque()
    frontier.append(start)
    explored = set()

    while frontier:
        current_state = frontier.popleft()

        #  Kiểm tra goal: xe 0 đi ngang, ra tới cột 5
        main_car = current_state.cars[0]
        if not main_car.vertical and main_car.coord[1] + main_car.length == 6:
            # Truy vết đường đi
            path = []
            while current_state != start:
                path.append(current_state)
                current_state = current_state.parent
            path.reverse()
            return path  

        explored.add(current_state.to_tuple())

        for next_state in current_state.next_states():
            state_tuple = next_state.to_tuple()
            if state_tuple not in explored:
                frontier.append(next_state)

    return None  # Không tìm thấy lời giải
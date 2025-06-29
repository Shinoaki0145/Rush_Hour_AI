from .state import *

def dls(state, explored, depth):
    # Kiểm tra goal: xe 0 đi ngang, ra tới cột 5
    if state.cars[0].coord[1] + state.cars[0].length == 6:
        return state
    if depth > 0:
        explored.add(state.to_tuple())
        for next_state in state.next_states():
            if next_state.to_tuple() not in explored:
                result = dls(next_state, explored, depth - 1)
                if result:
                    return result
    return None

def ids(start):
    max_depth = 50
    for depth in range(max_depth + 1):
        result = dls(start, set(), depth)
        if result:
            break

    path = []
    if result:
        while result != start:
            path.append(result)
            result = result.parent
        path.append(start)
        path.reverse()
    return path
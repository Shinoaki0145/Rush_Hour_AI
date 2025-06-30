from .state import *

state_count = 0

def dls(state, explored, depth):
    global state_count
    state_count += 1
    if depth > 0:
        explored.add(state.to_tuple())
        for next_state in state.next_states():
            # Kiểm tra goal: xe 0 đi ngang, ra tới cột 5
            if next_state.cars[0].coord[1] + next_state.cars[0].length == 6:
                return next_state
            if next_state.to_tuple() not in explored:
                result = dls(next_state, explored, depth - 1)
                if result:
                    return result
        explored.remove(state.to_tuple())
    return None

def ids(start):
    max_depth = 50
    for depth in range(max_depth + 1):
        result = dls(start, set(), depth)
        global state_count
        print(f"Depth: {depth}. Expanded nodes: {state_count}.")
        state_count = 0
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
from .state import *

state_count = 0

def dfs_recursive(state, explored):
    global state_count
    state_count += 1
    explored.add(state.to_tuple())
    for next_state in state.next_states():
        # Kiểm tra goal: xe 0 đi ngang, ra tới cột 5
        if next_state.cars[0].coord[1] + next_state.cars[0].length == 6:
            return next_state
        if next_state.to_tuple() not in explored:
            result = dfs_recursive(next_state, explored)
            if result:
                return result
    explored.remove(state.to_tuple())
    return None

def dfs(start):
    result = dfs_recursive(start, set())
    print(f"Expanded nodes: {state_count}")

    path = []
    if result:
        while result != start:
            path.append(result)
            result = result.parent
        path.append(start)
        path.reverse()
    return path
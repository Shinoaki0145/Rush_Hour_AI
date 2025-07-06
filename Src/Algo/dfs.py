from .state import *


def dfs_recursive(state, explored, state_count):
    state_count[0] += 1
    
    target_car = state.cars[0]
    if not target_car.vertical and target_car.coord[1] + target_car.length == 6:
        return state
    
    explored.add(state.to_tuple())
    for next_state in state.next_states():
        if next_state.to_tuple() not in explored:
            result = dfs_recursive(next_state, explored, state_count)
            if result:
                return result
    return None

def dfs(start):
    state_count = [0]
    target_car = start.cars[0]
    if not target_car.vertical and target_car.coord[1] + target_car.length == 6:
        print(f"Expanded nodes: {state_count[0]}")
        return [start]

    result = dfs_recursive(start, set(), state_count)
    print(f"Expanded nodes: {state_count[0]}")

    path = []
    if result:
        while result != start:
            path.append(result)
            result = result.parent
        path.append(start)
        path.reverse()
    return path
from .state import *

def dfs(start):
    state_count = 0
    target_car = start.cars[0]
    if not target_car.vertical and target_car.coord[1] + target_car.length == 6:
        print(f"Expanded nodes: {state_count}")
        return [start]

    dfs_stack = [start]
    explored = set()
    while dfs_stack:
        current_state = dfs_stack.pop()
        state_tuple = current_state.to_tuple()

        if state_tuple in explored:
            continue

        state_count += 1
        explored.add(state_tuple)
        for next_state in reversed(current_state.next_states()):
            if next_state.to_tuple() not in explored:
                target_car = next_state.cars[0]
                if not target_car.vertical and target_car.coord[1] + target_car.length == 6:
                    path = []
                    while next_state != start:
                        path.append(next_state)
                        next_state = next_state.parent
                    path.append(start)
                    path.reverse()
                    print(f"Expanded nodes: {state_count}")
                    return path
                dfs_stack.append(next_state)

    print(f"Expanded nodes: {state_count}")
    return None
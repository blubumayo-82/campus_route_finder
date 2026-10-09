# Breadth-First Search (BFS) algorithm to find the fewest-hops path between buildings.

from collections import deque


# Finds the shortest path (fewest hops) between a start and destination building.
def find_route(adjacency_list, start, destination, blocked_buildings):
    # If the start or destination building is blocked, no route is possible
    if start in blocked_buildings or destination in blocked_buildings:
        return [], {}, {}

    # If the start is already the destination, the route is just that building
    if start == destination:
        return [start], {start: 0}, {start: None}

    # Stage 1: Set up the queue and tracking dictionaries
    queue = deque([start])
    levels = {start: 0}
    parents = {start: None}

    # Stage 2: Take buildings from the queue and explore them
    while len(queue) > 0:
        current_building = queue.popleft()

        # Stop early once we reach the destination
        if current_building == destination:
            break

        # Stage 3: Check all connected neighbors of the current building
        for neighbor in adjacency_list.get(current_building, []):
            # Skip any neighbor that is marked as blocked
            if neighbor in blocked_buildings:
                continue

            # Stage 4: Mark unvisited neighbors and record where we came from
            if neighbor not in levels:
                levels[neighbor] = levels[current_building] + 1
                parents[neighbor] = current_building
                queue.append(neighbor)

    # Stage 5: Trace the path backward from destination to start using parents
    route = []
    if destination in parents:
        current_building = destination
        while current_building is not None:
            route.append(current_building)
            current_building = parents[current_building]

        # Reverse the list so it goes from start to destination
        route.reverse()

    return route, levels, parents

# Test script to verify the BFS pathfinding logic on various campus routes.

from graph_data import build_adjacency_list
from bfs import find_route


# Helper function to print test results clearly.
def run_test_case(test_name, start, destination, blocked_buildings):
    print(f"=== {test_name} ===")
    print(f"Start: {start}")
    print(f"Destination: {destination}")
    print(f"Blocked Buildings: {blocked_buildings}")

    campus_graph = build_adjacency_list()
    route, levels, parents = find_route(campus_graph, start, destination, blocked_buildings)

    if len(route) > 0:
        route_text = " -> ".join(route)
        hops = len(route) - 1
        print(f"Route Found ({hops} hops): {route_text}")
    else:
        print("Result: No route exists!")

    print(f"Total Buildings Explored: {len(levels)}")
    print()


if __name__ == "__main__":
    # Test 1: Gate to CICT (normal route)
    run_test_case(
        "Test 1: Gate to CICT",
        "Gate",
        "CICT",
        []
    )

    # Test 2: Gate to Gate (same start and destination)
    run_test_case(
        "Test 2: Gate to Gate",
        "Gate",
        "Gate",
        []
    )

    # Test 3: Library to Medina Bldg. (immediate neighbors)
    run_test_case(
        "Test 3: Library to Medina Bldg.",
        "Library",
        "Medina Bldg.",
        []
    )

    # Test 4: Gate to NSTP (longer route across campus)
    run_test_case(
        "Test 4: Gate to NSTP",
        "Gate",
        "NSTP",
        []
    )

    # Test 5: Gate to CICT with Medina Grounds blocked (finding a detour)
    run_test_case(
        "Test 5: Gate to CICT (Medina Grounds Blocked)",
        "Gate",
        "CICT",
        ["Medina Grounds"]
    )

    # Test 6: Gate to NSTP with CBA blocked (isolated destination)
    run_test_case(
        "Test 6: Gate to NSTP (CBA Blocked)",
        "Gate",
        "NSTP",
        ["CBA"]
    )

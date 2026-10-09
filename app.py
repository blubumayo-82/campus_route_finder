# Main Flask application file for running the web server and handling routes.

from flask import Flask, render_template, request
from graph_data import BUILDINGS, POSITIONS, build_adjacency_list
from bfs import find_route
from map_drawer import draw_map

app = Flask(__name__)

# Build the campus adjacency list once when the application server starts
campus_graph = build_adjacency_list()


# Main route for the route finder page, supporting GET to view and POST to calculate.
@app.route("/", methods=["GET", "POST"])
def index():
    start = None
    destination = None
    blocked_buildings = []
    route = None
    hops = 0
    sorted_levels = []
    error_message = None

    if request.method == "POST":
        start = request.form.get("start")
        destination = request.form.get("destination")
        # getlist collects all checked checkboxes with name "blocked_buildings" into a Python list
        blocked_buildings = request.form.getlist("blocked_buildings")

        # Edge Case 1: Start or destination is selected as closed
        if start in blocked_buildings:
            error_message = f"The start building '{start}' is marked as closed. Please uncheck it to find a route."
        elif destination in blocked_buildings:
            error_message = f"The destination building '{destination}' is marked as closed. Please uncheck it to find a route."
        # Edge Case 2: Start and destination are the same building
        elif start == destination:
            route = [start]
            hops = 0
            sorted_levels = [(0, [start])]
        # Standard case: Run BFS pathfinding
        else:
            route, levels, parents = find_route(campus_graph, start, destination, blocked_buildings)
            hops = len(route) - 1

            # Edge Case 3: No path exists due to blocked buildings
            if len(route) == 0:
                error_message = "No route found! The path to your destination is completely cut off by closed buildings."
            else:
                # Group buildings by their BFS discovery level
                grouped_levels = {}
                for building, level_number in levels.items():
                    if level_number not in grouped_levels:
                        grouped_levels[level_number] = []
                    grouped_levels[level_number].append(building)

                # Order levels from 0 upward for the presentation table
                for level_number in sorted(grouped_levels.keys()):
                    sorted_levels.append((level_number, grouped_levels[level_number]))

    # Generate the map image on every request (empty route if no valid route found or on GET)
    display_route = route if (route is not None and len(route) > 0) else []
    map_image = draw_map(campus_graph, POSITIONS, display_route, blocked_buildings)

    return render_template(
        "index.html",
        buildings=BUILDINGS,
        start=start,
        destination=destination,
        blocked_buildings=blocked_buildings,
        route=route,
        hops=hops,
        sorted_levels=sorted_levels,
        error_message=error_message,
        map_image=map_image,
    )


# Graph view route displaying the adjacency list and graph statistics.
@app.route("/graph")
def graph():
    total_buildings = len(campus_graph)

    # Count total neighbor entries across all buildings
    total_neighbor_entries = 0
    for neighbors in campus_graph.values():
        total_neighbor_entries = total_neighbor_entries + len(neighbors)

    # Since each walkway is stored twice (undirected graph), divide by 2
    total_edges = total_neighbor_entries // 2

    return render_template(
        "graph.html",
        campus_graph=campus_graph,
        total_buildings=total_buildings,
        total_edges=total_edges,
    )


if __name__ == "__main__":
    app.run(debug=True)

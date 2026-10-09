# Matplotlib script to draw the campus map and highlight the calculated route.

import base64
import io
import matplotlib

# Use the "Agg" backend so matplotlib works in headless environments without a display window
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Draws the campus map with walkways, buildings, highlights the route, and marks blocked buildings.
def draw_map(adjacency_list, positions, route, blocked_buildings):
    # Step 1: Create a new figure and axis for drawing
    fig, ax = plt.subplots(figsize=(10, 8))

    # Step 2: Draw all walkways once as thin light gray lines
    drawn_walkways = set()
    for building, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            # Sort the two building names to treat (A, B) and (B, A) as the same walkway
            walkway = tuple(sorted([building, neighbor]))
            if walkway not in drawn_walkways:
                drawn_walkways.add(walkway)
                start_x = positions[building][0]
                end_x = positions[neighbor][0]
                start_y = positions[building][1]
                end_y = positions[neighbor][1]
                ax.plot([start_x, end_x], [start_y, end_y], color="lightgray", linewidth=1.5, zorder=1)

    # Step 3: Draw all buildings as default dots with their names
    for building, (coord_x, coord_y) in positions.items():
        ax.scatter(coord_x, coord_y, color="steelblue", s=70, zorder=2)
        ax.text(coord_x, coord_y + 0.35, building, fontsize=8, ha="center", va="bottom")

    # Step 4: If a route exists, draw the path lines and highlight the route buildings
    if len(route) > 0:
        # Draw thick lines along the path
        for i in range(len(route) - 1):
            building_a = route[i]
            building_b = route[i + 1]
            path_x = [positions[building_a][0], positions[building_b][0]]
            path_y = [positions[building_a][1], positions[building_b][1]]
            ax.plot(path_x, path_y, color="dodgerblue", linewidth=3.5, zorder=3)

        # Draw colored dots for buildings on the route
        for i in range(len(route)):
            building_name = route[i]
            pos_x, pos_y = positions[building_name]

            # Start building is colored green
            if i == 0:
                ax.scatter(pos_x, pos_y, color="green", s=130, zorder=4)
            # Destination building is colored blue
            elif i == len(route) - 1:
                ax.scatter(pos_x, pos_y, color="blue", s=130, zorder=4)
            # In-between buildings are colored orange
            else:
                ax.scatter(pos_x, pos_y, color="orange", s=110, zorder=4)

    # Step 5: Draw blocked buildings as red dots marked with an X
    for building_name in blocked_buildings:
        if building_name in positions:
            bx, by = positions[building_name]
            # Red circle background
            ax.scatter(bx, by, color="red", s=120, zorder=5)
            # White X mark inside
            ax.scatter(bx, by, color="white", marker="x", s=70, linewidths=2, zorder=6)

    # Step 6: Clean up the plot boundaries and hide axes
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 15)
    ax.axis("off")

    # Step 7: Save the plot into an in-memory buffer as a PNG image
    image_buffer = io.BytesIO()
    fig.savefig(image_buffer, format="png", bbox_inches="tight")

    # Step 8: Close the figure to free memory and prevent server leaks
    plt.close(fig)

    # Step 9: Convert image bytes to a base64 string
    image_buffer.seek(0)
    image_base64 = base64.b64encode(image_buffer.getvalue()).decode("utf-8")

    return image_base64

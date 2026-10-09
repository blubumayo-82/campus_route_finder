# Campus graph data represented as an adjacency list dictionary and building coordinates.

# 1. List of all 20 buildings on campus
BUILDINGS = [
    "Gate",
    "HM Lab",
    "Sarigamit Court",
    "Admin Bldg.",
    "CSG",
    "Library",
    "CAHS",
    "OSA",
    "CAD",
    "NCEA",
    "Old CEA Bldg.",
    "CTEC",
    "CAS",
    "Automotive",
    "Medina Bldg.",
    "Medina Grounds",
    "CICT",
    "CBA",
    "NSTP",
    "Train",
]

# 2. List of walkways connecting buildings (each walkway listed once)
EDGES = [
    ("Gate", "HM Lab"),
    ("Gate", "Sarigamit Court"),
    ("HM Lab", "Admin Bldg."),
    ("HM Lab", "Sarigamit Court"),
    ("HM Lab", "CSG"),
    ("CSG", "Admin Bldg."),
    ("Admin Bldg.", "Automotive"),
    ("Admin Bldg.", "Medina Grounds"),
    ("Admin Bldg.", "Library"),
    ("Automotive", "CAS"),
    ("CAS", "CTEC"),
    ("CAS", "CICT"),
    ("CTEC", "Old CEA Bldg."),
    ("Old CEA Bldg.", "NCEA"),
    ("Old CEA Bldg.", "CBA"),
    ("NCEA", "CAD"),
    ("NCEA", "Train"),
    ("Train", "CBA"),
    ("CAD", "OSA"),
    ("CAD", "CICT"),
    ("OSA", "CAHS"),
    ("OSA", "Medina Bldg."),
    ("CAHS", "Library"),
    ("Library", "Medina Bldg."),
    ("Library", "Sarigamit Court"),
    ("Medina Bldg.", "Medina Grounds"),
    ("Medina Grounds", "CICT"),
    ("CICT", "CBA"),
    ("CBA", "NSTP"),
]

# 3. Approximate (x, y) coordinates for drawing each building on a 10x14 grid
POSITIONS = {
    "Gate": (2, 0),
    "HM Lab": (1, 2),
    "Sarigamit Court": (4, 1),
    "Admin Bldg.": (1, 5),
    "CSG": (2, 3),
    "Library": (6, 2),
    "CAHS": (9, 2),
    "OSA": (9, 5),
    "CAD": (9, 8),
    "NCEA": (9, 12),
    "Old CEA Bldg.": (5, 13),
    "CTEC": (1, 12),
    "CAS": (1, 10),
    "Automotive": (1, 7),
    "Medina Bldg.": (7, 4),
    "Medina Grounds": (4, 4),
    "CICT": (5, 7),
    "CBA": (5, 10),
    "NSTP": (4, 9),
    "Train": (7, 11),
}


# Builds and returns an adjacency list dictionary where each building maps to its connected neighbors.
def build_adjacency_list():
    # Create a dictionary with an empty list for every building
    adjacency_list = {}
    for building in BUILDINGS:
        adjacency_list[building] = []

    # Add each walkway in both directions because walking paths are two-way (undirected)
    for start_building, end_building in EDGES:
        adjacency_list[start_building].append(end_building)
        adjacency_list[end_building].append(start_building)

    return adjacency_list


if __name__ == "__main__":
    campus_graph = build_adjacency_list()
    for building, neighbors in campus_graph.items():
        neighbor_names = ", ".join(neighbors)
        print(f"{building}: {neighbor_names}")

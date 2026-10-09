# Campus Route Finder — Project Presentation & Study Guide

A beginner-friendly guide for first-year Data Science students to prepare and present our class project.

---

## 1. Project Overview
**Campus Route Finder** is a web application that calculates the shortest walking route (fewest walkway hops) between any two buildings on our campus. Written in pure Python without external graph libraries, the project stores the campus layout as an undirected graph using an **adjacency list** and uses a handwritten **Breadth-First Search (BFS)** algorithm to find routes. Users can pick buildings from a form, mark closed buildings to force realistic detours, review a step-by-step level table for algorithm demonstration, and view an automatically drawn visual map.

---

## 2. Project File Structure
- `app.py` — The Flask web server that handles user requests, runs BFS, and sends data to HTML pages.
- `graph_data.py` — Contains our 20 buildings, 29 walkway edges, grid coordinates, and builds the adjacency list.
- `bfs.py` — Implements our custom Breadth-First Search algorithm (`find_route`) to find the shortest path.
- `map_drawer.py` — Uses Matplotlib to draw campus buildings, walkways, highlighted routes, and outputs a base64 image.
- `test_bfs.py` — A standalone terminal script that tests multiple routing scenarios, including detours and blocked paths.
- `requirements.txt` — Lists the two required packages for the virtual environment: `flask` and `matplotlib`.
- `templates/base.html` — The base layout template containing the page header, navigation links, and container.
- `templates/index.html` — The main page template featuring dropdown selectors, closed building checkboxes, results, and the map.
- `templates/graph.html` — Displays the complete adjacency list table along with total node and walkway counts.
- `templates/about.html` — Explains how the BFS algorithm works and why an adjacency list was chosen.
- `static/style.css` — Plain CSS styling cards, form inputs, zebra-striped tables, and responsive elements.

---

## 3. How the Graph is Stored

### Tiny 4-Building Example
In Python, an **adjacency list** is simply a dictionary where each building maps to a list of its direct neighbors:
```python
campus_graph = {
    "Gate": ["Library", "Cafe"],
    "Library": ["Gate", "Canteen"],
    "Cafe": ["Gate", "Canteen"],
    "Canteen": ["Library", "Cafe"]
}
```

### How Our Real Graph is Built
1. We define each physical walkway once in a list called `EDGES` as a tuple, e.g., `("Gate", "HM Lab")`.
2. In `build_adjacency_list()`, we first give every building an empty list: `{"Gate": [], "HM Lab": [], ...}`.
3. We loop through each walkway in `EDGES` and add the connection **in both directions**:
   ```python
   adjacency_list[start_building].append(end_building)
   adjacency_list[end_building].append(start_building)
   ```
   This ensures that if you can walk from Gate to HM Lab, you can also walk from HM Lab to Gate.

---

## 4. BFS Explained Line by Line (`find_route`)

### Step-by-Step Logic
1. **Safety Checks**: If `start` or `destination` is closed, return no route. If `start == destination`, return `[start]`.
2. **Queue & Tracking**:
   ```python
   queue = deque([start])      # Queue holds buildings waiting to be explored
   levels = {start: 0}         # Records number of hops from start (also tracks visited)
   parents = {start: None}     # Records which building discovered each neighbor (breadcrumbs)
   ```
3. **Queue Loop**: While the queue has buildings:
   - `current_building = queue.popleft()` takes the oldest building (First-In, First-Out).
   - If `current_building == destination`, stop searching immediately.
4. **Neighbor Exploration**:
   - For every neighbor in `adjacency_list[current_building]`:
     - Skip if neighbor is in `blocked_buildings`.
     - If neighbor is not in `levels` (unvisited):
       - `levels[neighbor] = levels[current_building] + 1`
       - `parents[neighbor] = current_building`
       - `queue.append(neighbor)`
5. **Path Reconstruction**: Start at `destination`, step backward through `parents` until reaching `start` (`None`), then reverse the list.

### Traced Example: Gate to CICT
- **Initial State**: Queue = `[Gate]`, Levels = `{Gate: 0}`, Parents = `{Gate: None}`
- **Step 1**: Pop `Gate`. Add unvisited neighbors `HM Lab` and `Sarigamit Court`.  
  *Queue:* `[HM Lab, Sarigamit Court]`
- **Step 2**: Pop `HM Lab`. Add unvisited neighbors `Admin Bldg.` and `CSG`.  
  *Queue:* `[Sarigamit Court, Admin Bldg., CSG]`
- **Step 3**: Pop `Sarigamit Court`. Add unvisited neighbor `Library`.  
  *Queue:* `[Admin Bldg., CSG, Library]`
- **Step 4**: Pop `Admin Bldg.`. Add unvisited neighbors `Automotive` and `Medina Grounds`.  
  *Queue:* `[CSG, Library, Automotive, Medina Grounds]`
- **Step 5**: Pop `CSG` (all neighbors already visited).  
  *Queue:* `[Library, Automotive, Medina Grounds]`
- **Step 6**: Pop `Library`. Add unvisited neighbor `CAHS` and `Medina Bldg.`.  
  *Queue:* `[Automotive, Medina Grounds, CAHS, Medina Bldg.]`
- **Step 7**: Pop `Automotive`. Add unvisited neighbor `CAS`.  
  *Queue:* `[Medina Grounds, CAHS, Medina Bldg., CAS]`
- **Step 8**: Pop `Medina Grounds`. Discovers destination **`CICT`**! `CICT` gets parent `Medina Grounds` and enters queue.
- **Step 9**: When `CICT` is popped from the front, BFS breaks.
- **Traceback**: `CICT` &rarr; `Medina Grounds` &rarr; `Admin Bldg.` &rarr; `HM Lab` &rarr; `Gate`.  
- **Final Reversed Route**: `Gate -> HM Lab -> Admin Bldg. -> Medina Grounds -> CICT` (4 hops).

---

## 5. How a User Click Becomes a Result
1. **User Action**: The user selects `Gate` and `CICT` on the web page and clicks **"Find Route"**.
2. **HTTP POST to Flask (`app.py`)**: The browser sends the form values to the `@app.route("/")` function.
3. **Algorithm Execution (`bfs.py`)**: Flask calls `find_route(campus_graph, "Gate", "CICT", blocked)`. BFS runs and returns the route and levels.
4. **Map Rendering (`map_drawer.py`)**: Matplotlib plots the nodes, draws the path in thick blue, converts the drawing to a **base64 text string**, and closes the figure.
5. **Template Rendering (`index.html`)**: Flask feeds the route, level table, and image text into Jinja, which builds the HTML page and sends it back to the browser screen.

---

## 6. Time Complexity in Simple Terms ($O(V + E)$)
- **$V$ (Vertices / Buildings)** = 20
- **$E$ (Edges / Walkways)** = 29
- Each building is placed into the queue and popped at most once: **$O(V)$**.
- Each walkway is checked at most twice (once from each end): **$O(E)$**.
- **Total Time Complexity**: $\mathcal{O}(V + E)$.
- **Why this is great for our campus**: With $V = 20$ and $E = 29$, BFS executes roughly $20 + 58 = 78$ basic operations, taking less than 1 millisecond. Even if our campus grew to 1,000 buildings, BFS would run instantaneously.

---

## 7. 10 Questions a Professor Might Ask (with Short Answers)

1. **Why use Breadth-First Search (BFS) instead of Depth-First Search (DFS)?**  
   *Answer:* BFS explores level by level (like ripples in a pond), guaranteeing the route with the fewest hops. DFS explores down one path as deep as possible and often returns excessively long, convoluted routes.

2. **Why an adjacency list instead of an adjacency matrix?**  
   *Answer:* Our campus graph is sparse (few edges per node). An adjacency matrix would store a 20×20 grid (400 entries) mostly filled with zeros. An adjacency list uses less memory and provides direct access to connected neighbors in $O(1)$ time.

3. **Why is the graph undirected?**  
   *Answer:* Campus walkways allow two-way pedestrian traffic. If you can walk from Gate to HM Lab, you can walk back from HM Lab to Gate.

4. **How does the algorithm handle closed/blocked buildings?**  
   *Answer:* When BFS checks a building's neighbors, it checks `if neighbor in blocked_buildings: continue`. It skips closed buildings entirely, forcing the search to discover an alternate detour.

5. **What happens if no route exists between two buildings?**  
   *Answer:* The queue empties without ever finding the destination. Because the destination is never added to the `parents` dictionary, `find_route` returns an empty list `[]`, and Flask shows a friendly "No route found" message.

6. **Why use `collections.deque` instead of a standard Python `list` for the queue?**  
   *Answer:* Popping the first element of a regular list (`list.pop(0)`) takes $O(N)$ time because all subsequent items must shift left. A `deque.popleft()` operates in $O(1)$ constant time.

7. **How does BFS prevent infinite loops on a campus with circular walkway loops?**  
   *Answer:* By checking `if neighbor not in levels:`. Once a building has been reached and assigned a level, it is never added to the queue again.

8. **Why trace backward using the `parents` dictionary instead of building the route forward?**  
   *Answer:* BFS explores multiple paths at the same time. We do not know which branch reaches the destination until we arrive there. Tracing backward from destination to parent to grandparent guarantees a single, direct path back to the start.

9. **Why send the map as a base64 image string instead of saving a PNG file to the hard drive?**  
   *Answer:* Base64 keeps the server stateless and fast. We don't fill the server's disk with temporary files, and the browser receives the image directly inside the HTML response without making a second request.

10. **Does BFS guarantee the shortest physical distance in meters?**  
    *Answer:* No. BFS guarantees the path with the **fewest hops** (walkway segments). Because our edges are unweighted, BFS treats all walkways as having equal length.

---

## 8. Limitations & Future Improvements
1. **Unweighted Walkways**: Currently, a 10-meter walkway counts the same as a 100-meter walkway. *Future improvement:* Add distance weights in meters and upgrade to Dijkstra's algorithm.
2. **Accessibility Features**: Some walkways may have stairs. *Future improvement:* Add an "Accessible / Ramp Only" filter for wheelchair users.
3. **Indoor Floor Routing**: Currently, the map only routes between exterior building doors. *Future improvement:* Add multi-floor interior room navigation.
4. **Interactive Map**: The current map is a static Matplotlib image. *Future improvement:* Use an interactive JavaScript map library (like Leaflet.js) to allow zooming, panning, and GPS user location.

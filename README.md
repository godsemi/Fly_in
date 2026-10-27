*This project has been created as part of the 42 curriculum by jopaz-su.*

# Fly-in

## Description

**Fly-in** is a drone routing and traffic simulation system developed in Python. The goal is to move a fleet of drones from a starting zone to a destination through a network of interconnected zones while minimizing the total number of simulation turns.

The network is represented as a graph, where zones are vertices and connections are edges. Each zone and connection can have specific properties, such as movement costs, occupancy limits, and connection capacities. These constraints affect route selection and determine whether a drone can move during a given turn.

The project combines graph traversal, shortest-path algorithms, resource management, and turn-based simulation to coordinate multiple drones efficiently.

### Main features

- **Map parsing and validation:** Reads a map file defining the number of drones, zones, connections, and their metadata.
- **Graph exploration:** Uses Depth-First Search (DFS) with backtracking to discover possible routes.
- **Shortest-path calculation:** Implements Dijkstra's algorithm using a priority queue to find low-cost paths.
- **Route assignment:** Selects routes for drones before the simulation begins.
- **Turn-based simulation:** Coordinates drone movements while respecting zone occupancy, connection capacity, and zone-specific restrictions.
- **Colored terminal output:** Uses ANSI escape codes to distinguish zone types and drone identifiers.
- **Code quality:** Uses Python type annotations and supports linting and static type checking.

## Instructions

### Requirements

- Python 3.10 or later.
- GNU Make.
- A terminal compatible with ANSI escape codes for colored output.

### Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/godsemi/Fly_in.git
cd Fly_in
```

Install the project dependencies:

```bash
make install
```

This command creates a virtual environment in `.venv` and installs the required dependencies.

### Running the simulation

Run the program with a map file:

```bash
make run MAP=<map_file>
```

For example:

```bash
make run MAP=example.map
```

Replace `example.map` with the path to your own map file.

### Debug mode

Run the simulation in debug mode to help investigate the program's behaviour:

```bash
make debug MAP=example.map
```

### Code quality

Run the standard linting checks:

```bash
make lint
```

For stricter static type checking:

```bash
make lint-strict
```

### Cleanup

Remove generated files and other artifacts handled by the Makefile:

```bash
make clean
```

## Map File Format

The map file defines the drone fleet, the zones in the network, and the connections between them.

Each entry must follow the syntax expected by the parser.

### Basic structure

```text
nb_drones: <number>
start_hub: <name> <x> <y> [metadata]
end_hub: <name> <x> <y> [metadata]
hub: <name> <x> <y> [metadata]
connection: <zone1>-<zone2> [metadata]
```

- `nb_drones`: Number of drones participating in the simulation.
- `start_hub`: Starting zone, including its name and coordinates.
- `end_hub`: Destination zone, including its name and coordinates.
- `hub`: An intermediate zone.
- `connection`: A connection between two zones. The network is defined by these connections.

The optional metadata allows the behaviour of zones and connections to be configured.

### Zone metadata

| Option | Description |
| --- | --- |
| `zone=<type>` | Defines the zone type. |
| `color=<value>` | Specifies the zone's display color. |
| `max_drones=<number>` | Sets the maximum number of drones allowed in the zone. |

### Connection metadata

| Option | Description |
| --- | --- |
| `max_link_capacity=<number>` | Sets the maximum number of drones allowed on a connection simultaneously. |

### Zone types

| Type | Description |
| --- | --- |
| `normal` | Standard zone with a movement cost of 1. |
| `priority` | Preferred zone with a movement cost of 0 during pathfinding. |
| `restricted` | Zone that requires additional transit time. |
| `blocked` | Zone excluded from valid routes. |

The parser is responsible for interpreting the map and validating its contents before the routing and simulation stages begin.

## Algorithm Design and Implementation

The project is organized into several stages. Each stage has a specific responsibility, separating input processing, graph algorithms, route selection, and simulation.

### 1. Map parsing and validation

The parser reads the input map and extracts the drone count, start and end zones, intermediate zones, connections, and associated metadata.

The parsed information is used to construct the graph on which the routing algorithms operate. Separating parsing from pathfinding allows the algorithms to work with structured data rather than raw text.

Invalid map data should be rejected before the simulation starts, preventing malformed input from propagating into later stages.

### 2. Graph representation

The network is represented as a graph:

- **Vertices:** Zones that drones can occupy.
- **Edges:** Connections through which drones can travel.
- **Zone properties:** Movement costs, occupancy limits, and restrictions.
- **Connection properties:** Capacity limits controlling simultaneous traffic.

This representation makes it possible to explore the network, calculate routes, and enforce movement constraints during the simulation.

### 3. Route discovery with Depth-First Search

Depth-First Search explores the graph by following a connection to an unvisited zone and continuing until it reaches the destination or cannot proceed.

Backtracking allows the algorithm to return to previous zones and explore alternative branches.

Blocked zones are excluded from valid routes.

DFS is useful for discovering possible paths, but it does not guarantee the shortest or cheapest route. For that reason, route discovery and shortest-path calculation are handled as distinct algorithmic tasks.

### 4. Shortest-path calculation with Dijkstra's algorithm

Dijkstra's algorithm calculates a minimum-cost path through the graph using accumulated movement costs.

A minimum-heap priority queue, implemented with Python's `heapq` module, selects the next zone with the lowest currently known path cost.

The algorithm relaxes the available connections, updating the best-known cost and predecessor information whenever a cheaper path is found.

Movement costs depend on the destination zone type. In particular, priority zones have a cost of 0, while normal zones have a cost of 1.

This approach avoids exploring paths in arbitrary order and provides an efficient way to determine a minimum-cost route when the configured costs are non-negative.

### 5. Route assignment

Once the available routes and their costs have been calculated, the route assignment stage determines which paths will be used by the drones.

The objective is to choose suitable routes based on their associated costs while preparing the drones for the simulation.

Routes are assigned before movement begins and stored in each drone's state. This avoids recalculating the same route at every simulation turn and separates route planning from movement execution.

The selected paths still have to respect the dynamic constraints of the simulation. A valid route does not necessarily mean that a drone can traverse it immediately, since other drones may occupy zones or use connections.

### 6. Turn-based simulation

The simulation advances in discrete turns. During each turn, the program determines which drones can move to their next zones without violating the network's constraints.

The simulation accounts for:

- Zone occupancy and maximum capacity.
- Connection capacity and simultaneous traffic.
- Zone-specific movement restrictions.
- The current position and planned route of every drone.
- Additional transit time associated with restricted zones.

Zone occupancy and connection usage are tracked to prevent conflicting movements.

When a drone leaves a zone, that zone may become available to another drone during the same turn, depending on the simulation's movement-processing rules. This helps avoid unnecessary delays while preserving capacity constraints.

Restricted zones require additional transit time, so entering one may affect when a drone can continue its journey.

The simulation continues until the drones reach the destination, subject to the program's completion and error-handling conditions.

### Algorithmic strategy

The implementation combines different techniques because each solves a different problem:

| Technique | Purpose |
| --- | --- |
| Graph representation | Models zones and connections. |
| DFS with backtracking | Explores possible routes. |
| Dijkstra's algorithm | Calculates minimum-cost paths. |
| `heapq` priority queue | Efficiently selects the next lowest-cost candidate. |
| Route assignment | Prepares drone paths before simulation. |
| Turn-based simulation | Coordinates movements and manages shared capacity constraints. |

A key design decision is to separate **static planning** from **dynamic execution**. Pathfinding works with the graph and its movement costs, whereas the simulation handles changing occupancy and connection usage.

This separation improves modularity and avoids repeating pathfinding calculations on every turn.

## Example

The following example illustrates a small network with two drones and two alternative routes.

### Input

Save the following as `example.map`:

```text
nb_drones: 2
start_hub: A 0 0
hub: B 1 0
hub: C 1 1
end_hub: D 2 0
connection: A-B
connection: B-D
connection: A-C
connection: C-D
```

This network contains two routes from `A` to `D`:

- `A → B → D`
- `A → C → D`

Both routes contain two connections, and all zones are normal zones by default.

### Execution

```bash
make run MAP=example.map
```

### Expected result

Both drones should eventually reach zone `D`, provided the map is accepted by the parser and no additional constraints prevent their movements.

A conceptual movement sequence could look like this:

```text
Turn 1: D1 moves A -> B
        D2 moves A -> C

Turn 2: D1 moves B -> D
        D2 moves C -> D

Result: All drones have reached the destination.
```

This is an illustrative representation of the expected behaviour, not a guaranteed literal transcript of the program's terminal output. The actual movement order and number of turns depend on the implementation's movement rules, capacity constraints, and output format.

## Visual Representation

Fly-in uses colored terminal output to make the network and simulation easier to understand.

ANSI escape codes allow text to be displayed in different colors without requiring a graphical interface or an external rendering library.

### Zone colors

| Zone type | Color | Meaning |
| --- | --- | --- |
| `normal` | White | Standard zone. |
| `priority` | Green | Preferred zone during pathfinding. |
| `restricted` | Yellow | Zone with additional transit time. |
| `blocked` | Red | Zone excluded from valid routes. |

Drone identifiers are displayed in cyan to distinguish them from zone information.

### How the visualization improves usability

- **Faster identification:** Color coding makes it easier to distinguish zone types at a glance.
- **Improved readability:** Drone identifiers stand out from the surrounding output.
- **Easier debugging:** Restricted and blocked zones can be identified quickly when examining route selection and movement behaviour.
- **Better simulation tracking:** Colored output makes the progress of the simulation easier to follow during execution.

The visualization is designed for terminals that support ANSI escape codes, including typical Linux, macOS, and WSL terminals.

## Project Structure

```text
Fly_in/
├── main.py          # Program entry point
├── parser.py        # Map parsing and validation
├── parse_raise.py   # Parsing exceptions
├── graph.py         # Graph representation
├── pathfinding.py   # Graph traversal and pathfinding
├── simulation.py    # Simulation and route assignment
├── drones.py        # Drone state and movement
├── zones.py         # Zone definitions and properties
├── connection.py    # Connection definitions and capacity
├── colour.py        # Terminal color formatting
└── Makefile         # Installation, execution and quality checks
```

### Technical concepts

The project applies the following programming and computer science concepts:

- Graph theory and graph traversal.
- Depth-First Search and backtracking.
- Dijkstra's shortest-path algorithm.
- Priority queues and heap-based selection.
- Turn-based multi-agent simulation.
- Resource and capacity management.
- Modular programming and separation of responsibilities.
- Python type annotations and static type checking.

## Resources

The following resources provide further information about the algorithms, language features, and tools used in the project.

### Python documentation

- [Python documentation](https://docs.python.org/3/) — Official reference for the Python language and standard library.
- [`heapq` — Heap queue algorithm](https://docs.python.org/3/library/heapq.html) — Documentation for the priority queue used by Dijkstra's algorithm.
- [Python typing](https://docs.python.org/3/library/typing.html) — Type annotations and support for static analysis.

### Algorithms and graph theory

- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) — Explanation of minimum-cost pathfinding.
- [Depth-first search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search) — Explanation of graph exploration and backtracking.
- [Introduction to Algorithms — MIT OpenCourseWare](https://ocw.mit.edu/) — Educational material covering algorithms and data structures.

### Code quality and terminal output

- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/) — Guidelines for documenting Python modules, classes, and functions.
- [mypy documentation](https://mypy.readthedocs.io/) — Static type checking for Python.
- [GNU Make manual](https://www.gnu.org/software/make/manual/) — Reference for the project's build and task automation.

### AI usage

AI assistance was used to help structure and improve this README, including:

- Organizing the documentation into clear sections.
- Improving explanations of the project's algorithms and implementation strategy.
- Preparing illustrative examples of map input and expected simulation behaviour.
- Improving the clarity and readability of the technical documentation.

AI assistance was used for documentation drafting in this README. This description does not imply that AI generated, modified, or tested the project's source code.

The implementation, algorithm behaviour, example output, and technical claims should be checked against the actual source code before submission.


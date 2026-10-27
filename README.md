*This project has been created as part of the 42 curriculum by jopaz-su.*

Fly-in

Description

Fly-in is a drone routing simulation system developed in Python. The goal is to move a fleet of drones from a starting zone to a destination through a network of connected zones, while minimizing the total number of simulation turns.

The system parses a map file describing the network, identifies possible routes using Depth-First Search (DFS), calculates shortest paths using Dijkstra's algorithm, and simulates drone movement turn by turn while taking zone occupancy and connection capacity into account.

Instructions

Requirements

Python 3.10 or later

GNU Make

Installation

make install

This creates a virtual environment in .venv and installs the project dependencies.

Running

make run MAP=<map_file>

Example:

make run MAP=example.map

Debug mode

make debug MAP=<map_file>

Linting

make lint

For stricter type checking:

make lint-strict

Cleanup

make clean

Map File Format

Maps describe the drone count, zones and connections that form the network.

nb_drones: <number>
start_hub: <name> <x> <y> [metadata]
end_hub: <name> <x> <y> [metadata]
hub: <name> <x> <y> [metadata]
connection: <zone1>-<zone2> [metadata]

Zone metadata

Option

Description

zone=<type>

Defines the zone type

color=<value>

Defines the zone color

max_drones=<number>

Sets the maximum number of drones allowed in the zone

Connection metadata

Option

Description

max_link_capacity=<number>

Sets the maximum number of drones allowed on a connection simultaneously

Zone types

Type

Description

normal

Standard zone with a movement cost of 1

priority

Preferred zone with a movement cost of 0 in pathfinding

restricted

Zone that requires additional time to traverse

blocked

Zone excluded from valid routes

Algorithms

Pathfinding

Depth-First Search (DFS)

DFS explores the network recursively, using backtracking to discover possible paths between the starting and destination zones. Blocked zones are excluded from valid routes.

Dijkstra's Algorithm

Dijkstra calculates a shortest path based on accumulated movement costs. A minimum-heap priority queue (heapq) is used to select the next zone to explore, while movement costs depend on the destination zone type.

Path Assignment

The path assignment stage calculates routes for the drones and uses their associated costs to determine route preferences.

Simulation

The simulation processes drone movements turn by turn. Movement validation takes zone occupancy, connection capacity and zone-specific restrictions into account.

During each turn:

Zone occupancy and connection usage are tracked.

Each drone checks whether its next movement is valid.

Capacity constraints determine whether a drone can move.

Drones release their current zones when they move, potentially allowing other drones to use those zones during the same turn.

Restricted zones require additional transit time.

Paths are assigned before the simulation starts and stored with the drone state to avoid recalculating them during every turn.

Project Structure

Fly_in/
├── main.py          # Program entry point
├── parser.py        # Map parsing and validation
├── parse_raise.py   # Parsing exceptions
├── graph.py         # Graph representation
├── pathfinding.py   # Pathfinding algorithms
├── simulation.py    # Simulation and route assignment
├── drones.py        # Drone state and movement
├── zones.py         # Zone definitions and properties
├── connection.py    # Connection definitions and capacity
├── colour.py        # Terminal color formatting
└── Makefile         # Project commands

Technical Concepts

Graph representation and traversal

Depth-First Search with backtracking

Dijkstra's shortest-path algorithm

Priority queues using heapq

Turn-based multi-agent simulation

Resource and capacity management

Python type annotations and static type checking

Visual Representation

The simulation uses ANSI escape codes to display colored output in compatible terminals.

Zone type

Color

normal

White

priority

Green

restricted

Yellow

blocked

Red

Drone identifiers are displayed in cyan.

Supported terminals include Linux, macOS and WSL terminals with ANSI color support.

Resources

Python heapq documentation

Dijkstra's algorithm

Depth-first search

ANSI escape codes

PEP 257 — Docstring Conventions

mypy documentation
from graph import Graph
from zones import Zone
import heapq
from typing import Optional


def search_paths(
        graph: Graph, current: str, end: str, viewed: set[str],
        path: list[str], all: list[list[str]]
        ) -> None:
    """Recursively find all valid paths between two zones."""

    if current == end:
        all.append(list(path))
        return
    neighborhood = graph.get_neighbors(current)

    for neighbor in neighborhood:
        neighbor_zone = graph.get_zone(neighbor)
        if (neighbor not in viewed and neighbor_zone is not None
                and neighbor_zone.type_zone != "blocked"):
            path.append(neighbor)
            viewed.add(neighbor)
            search_paths(graph, neighbor, end, viewed, path, all)
            path.pop()
            viewed.remove(neighbor)


def find_paths(graph: Graph, start: Zone, end: Zone) -> list[list[str]]:
    """Find all valid paths between a start zone and an end zone."""
    all_paths: list[list[str]] = []
    search_paths(graph, start.name, end.name,
                 {start.name}, [start.name], all_paths)
    return all_paths


def algorithm(graph: Graph, start: Zone, end: Zone) -> list[str]:
    """Find the lowest-cost path using Dijkstra's algorithm.
    Each zone type has a different traversal cost. Blocked zones
    are excluded, while priority zones have zero traversal cost."""
    costs: dict[str, float] = {"normal": 1, "restricted": 2,
                               "priority": 0, "blocked": float('inf')}
    zone_cost: dict[str, float] = {start.name: 0}
    previous: dict[str, str] = {}
    queue: list[tuple[float, str]] = []
    heapq.heappush(queue, (0, start.name))
    while queue:
        cost, zone = heapq.heappop(queue)
        if cost > zone_cost.get(zone, float('inf')):
            continue
        if zone == end.name:
            break
        for neighbor in graph.get_neighbors(zone):
            neighbor_zone = graph.get_zone(neighbor)
            if neighbor_zone is None:
                continue
            move_cost = costs.get(neighbor_zone.type_zone, float('inf'))
            if move_cost == float('inf'):
                continue
            total_cost = cost + move_cost
            if total_cost < zone_cost.get(neighbor, float('inf')):
                zone_cost[neighbor] = total_cost
                previous[neighbor] = zone
                heapq.heappush(queue, (total_cost, neighbor))

    current: Optional[str] = end.name
    path: list[str] = []
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    if path and path[0] == start.name:
        return path
    return []

from drones import Drone
from graph import Graph
from pathfinding import find_paths
from colour import Colours


class Simulation:

    def __init__(self, graph: Graph) -> None:
        """Initialize a simulation for the given graph."""
        self.graph = graph
        self.drones: list[Drone] = []
        self.current_turn: int = 0
        self.history_movement: list[str] = []

    @staticmethod
    def path_cost(graph: Graph, path: list[str]) -> float:
        """Calculate the total traversal cost of a path."""
        costs: dict[str, float] = {
            "normal": 1, "restricted": 2, "priority": 0,
            "blocked": float('inf')
        }
        total: float = 0
        for zone_name in path[1:]:
            zone = graph.get_zone(zone_name)
            if zone is not None:
                total += costs.get(zone.type_zone, 1)
        return total

    def assign_path(self) -> None:
        """Assign paths to all drones in the simulation."""
        all_paths = find_paths(
            self.graph, self.graph.start, self.graph.end
        )
        sorted_costs = sorted(all_paths,
                              key=lambda p: self.path_cost(self.graph, p))
        for i in range(self.graph.nb_drones):
            path = sorted_costs[i % len(sorted_costs)]
            drone = Drone(assigned_path=path, identifier=f"D{i + 1}")
            self.drones.append(drone)

    def mov_validator(self, drone: Drone, occupied_zone: dict[str, int],
                      connection_use: dict[tuple[str, str], int]) -> bool:
        """Check whether a drone can move to its next zone."""
        next_zone_name = drone.get_next_zone
        if next_zone_name is None:
            return False
        next_zone = self.graph.get_zone(next_zone_name)
        if next_zone is None:
            return False
        if not next_zone.is_end:
            if occupied_zone.get(next_zone_name, 0) >= next_zone.max_drones:
                return False
        connection = self.graph.get_connection(drone.actual_zone,
                                               next_zone_name)
        if connection is None:
            return False
        max_cap: int = connection.link_capacity if (
            connection.link_capacity is not None)else 1
        connection_key: tuple[str, str] = (
            min(drone.actual_zone, next_zone_name),
            max(drone.actual_zone, next_zone_name)
        )
        if connection_use.get(connection_key, 0) >= max_cap:
            return False

        return True

    def simulate_turn(self) -> list[str]:
        """Simulate one turn and update drone movements."""
        movement: list[str] = []
        occupied_zone: dict[str, int] = {
            zone_name: sum(1 for d in self.drones
                           if d.actual_zone == zone_name and not
                           d.has_finished and not
                           self.graph.zones[zone_name].is_start)
            for zone_name in self.graph.zones
        }
        connection_use: dict[tuple[str, str], int] = {}
        for drone in self.drones:
            if drone.has_finished:
                continue
            if self.mov_validator(drone, occupied_zone, connection_use):
                actual_zone_name = drone.actual_zone
                next_zone_name = drone.get_next_zone
                if next_zone_name is None:
                    continue
                next_zone = self.graph.get_zone(next_zone_name)
                next_restricted = (
                    next_zone is not None and
                    next_zone.type_zone == "restricted"
                )
                drone.movement(next_restricted=next_restricted)
                drone_str = Colours.drone_colour(drone.identifier)
                if drone.transiting:
                    conn_name = (
                        f"{min(actual_zone_name, next_zone_name)}"
                        f"_{max(actual_zone_name, next_zone_name)}"
                    )
                    movement.append(f"{drone_str}-{conn_name}")
                else:
                    actual_zone = self.graph.get_zone(drone.actual_zone)
                    if actual_zone is not None:
                        zone_str = Colours.colour_exit(actual_zone)
                        movement.append(f"{drone_str}-{zone_str}")
        self.current_turn += 1
        if movement:
            self.history_movement.append(" ".join(movement))
            return movement

    def loop_turn(self) -> int:
        """Run simulation turns until all drones finish or the
        maximum turn limit is exceeded."""
        turns = len(self.drones) * len(self.graph.zones) * 10
        while any(not drone.has_finished for drone in self.drones):
            self.simulate_turn()
            if self.current_turn > turns:
                break
            return len(self.history_movement)

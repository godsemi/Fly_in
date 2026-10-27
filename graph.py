from typing import Optional
from zones import Zone
from connection import Connection
from parse_raise import PR


class Graph:

    def __init__(self, nb_drones: int) -> None:
        """Initialize an empty graph for the drone simulation."""
        self.nb_drones = nb_drones
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start: Optional[Zone] = None
        self.end: Optional[Zone] = None
        self.connection_keys: set[tuple[str, str]] = set()
        self.adjacent: dict[str, list[Connection]] = {}

    def get_zone(self, name: str) -> Optional[Zone]:
        """Retrieve a zone by its name."""
        return self.zones.get(name)

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the graph and register its connections."""
        if zone.name in self.zones:
            raise PR("Error: zone exists")

        self.zones[zone.name] = zone

        if zone.is_start:
            if self.start is not None:
                raise PR("Error: duplicated start")
            self.start = zone

        if zone.is_end:
            if self.end is not None:
                raise PR("Error: duplicated end")
            self.end = zone

        self.adjacent[zone.name] = []

    def add_connection(self, connection: Connection) -> None:
        """Add a connection between two existing zones."""
        if (connection.name1 not in self.zones or
                connection.name2 not in self.zones):
            raise PR("Error: Non existing zone detected.")

        valid_keys: tuple[str, str] = (
            min(connection.name1, connection.name2),
            max(connection.name1, connection.name2)
        )

        if valid_keys in self.connection_keys:
            raise PR(
                f"Error: connection already exists: "
                f"{connection.name1}, {connection.name2}."
            )

        if connection.name1 == connection.name2:
            raise PR("Error: Duplicated zone given.")

        self.connections.append(connection)
        self.connection_keys.add(valid_keys)

        self.adjacent[connection.name1].append(connection)
        self.adjacent[connection.name2].append(connection)

    def get_neighbors(self, name: str) -> list[str]:
        """Get the names of all zones adjacent to a given zone."""
        neighbors: list[str] = []

        for connection in self.adjacent[name]:
            neighbors.append(connection.return_other(name))

        return neighbors

    def get_connection(
        self,
        name1: str,
        name2: str
    ) -> Optional[Connection]:
        """Find the connection between two zones."""
        for connection in self.adjacent[name1]:
            if connection.valid_name(name2):
                return connection

        return None

    def validate(self) -> None:
        """Check that the graph has a start zone and an end zone."""
        if self.start is None:
            raise PR("Error: No start defined.")

        if self.end is None:
            raise PR("Error: No end defined.")

    def __repr__(self) -> str:
        """Return a readable summary of the graph."""
        return (
            f"Graph(zones={len(self.zones)}, "
            f"connections={len(self.connections)})"
        )

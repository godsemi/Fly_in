from zones import Zone
from graph import Graph
from connection import Connection
from parse_raise import PR


def drone_parser(line: str, nb: int) -> int:
    """parses the drones"""
    parsed = line.strip()

    if ":" not in parsed:
        raise PR(
            f"Line {nb}: expected 'nb_drones: <number>'"
        )

    key, value = parsed.split(":", 1)

    if key.strip() != "nb_drones":
        raise PR(
            f"Line {nb}: expected 'nb_drones:', got '{key.strip()}:'"
        )

    try:
        number = int(value.strip())
    except ValueError:
        raise PR(
            f"Line {nb}: nb_drones must be greater than 0"
        )

    if number <= 0:
        raise PR(
            f"Line {nb}: nb_drones must be greater than 0"
        )

    return number


def metadata_parser(metadata: str, nb: int) -> dict[str, str]:
    """parses the metadata"""
    metadata = metadata.strip()

    if not metadata.startswith("[") or not metadata.endswith("]"):
        raise PR(
            f"The metadata input '{metadata}' in line {nb} is incorrect"
        )

    data = metadata[1:-1].strip()

    if not data:
        raise PR(
            f"The metadata input '{metadata}' in line {nb} is incorrect"
        )

    meta: dict[str, str] = {}

    for item in data.split():
        if "=" not in item:
            raise PR(
                f"The metadata input '{metadata}' in line {nb} is incorrect"
            )

        key, value = item.split("=", 1)

        key = key.strip()
        value = value.strip()

        if not key or not value:
            raise PR(
                f"The metadata input '{metadata}' in line {nb} is incorrect"
            )

        if key in meta:
            raise PR(
                f"Duplicate metadata '{key}' in line {nb}"
            )

        meta[key] = value

    return meta


def zone_parser(line: str, nb: int) -> Zone:
    """parses the zones"""
    parsed = line.strip()

    if ":" not in parsed:
        raise PR(f"Line {nb}: missing ':'")

    zone_type, zone_info = parsed.split(":", 1)

    zone_type = zone_type.strip()
    zone_info = zone_info.strip()

    valid_zone_types = ("hub", "start_hub", "end_hub")

    if zone_type not in valid_zone_types:
        raise PR(
            f"Line {nb}: invalid zone type '{zone_type}'"
        )

    metadata: dict[str, str] = {}

    if "[" in zone_info:
        start = zone_info.find("[")

        if not zone_info.endswith("]"):
            raise PR(
                f"The metadata input in line {nb} is incorrect"
            )

        meta_info = zone_info[start:]
        zone_info = zone_info[:start].strip()

        metadata = metadata_parser(meta_info, nb)

    elif "]" in zone_info:
        raise PR(
            f"The metadata input in line {nb} is incorrect"
        )

    parameters = zone_info.split()

    if len(parameters) != 3:
        raise PR(
            f"Line {nb}: zone format must be '<name> <x> <y>'"
        )

    name, x_str, y_str = parameters

    if "-" in name:
        raise PR(
            f"Line {nb}: names cannot contain '-'"
        )

    try:
        x = int(x_str)
        y = int(y_str)
    except ValueError:
        raise PR(
            f"Line {nb}: x and y must be integers"
        )

    color = metadata.get("color")

    drones_number = metadata.get("max_drones", "1")

    try:
        max_drones = int(drones_number)
    except ValueError:
        raise PR(
            f"Line {nb}: max_drones must be a positive integer"
        )

    if max_drones <= 0:
        raise PR(
            f"Line {nb}: max_drones must be a positive integer"
        )

    zone_category = metadata.get("zone", "normal")

    valid_categories = {
        "normal",
        "blocked",
        "restricted",
        "priority"
    }

    if zone_category not in valid_categories:
        raise PR(
            f"Line {nb}: invalid zone type '{zone_category}'"
        )

    return Zone(
        name=name,
        x=x,
        y=y,
        type_zone=zone_category,
        color=color,
        max_drones=max_drones,
        is_start=(zone_type == "start_hub"),
        is_end=(zone_type == "end_hub")
    )


def connection_parser(line: str, nb: int, graph: Graph) -> None:
    """parses the connections"""
    parsed = line.strip()

    if ":" not in parsed:
        raise PR(
            f"Line {nb}: missing ':' in connection definition"
        )

    connection_type, connection_info = parsed.split(":", 1)

    connection_type = connection_type.strip()
    connection_info = connection_info.strip()

    if connection_type != "connection":
        raise PR(
            f"Line {nb}: invalid connection input"
        )

    metadata: dict[str, str] = {}

    if "[" in connection_info:
        start = connection_info.find("[")

        if not connection_info.endswith("]"):
            raise PR(
                f"Line {nb}: invalid metadata input"
            )

        meta_info = connection_info[start:]
        connection_info = connection_info[:start].strip()

        metadata = metadata_parser(meta_info, nb)

    elif "]" in connection_info:
        raise PR(
            f"Line {nb}: invalid metadata input"
        )

    parameters = connection_info.split("-")

    if len(parameters) != 2:
        raise PR(
            f"Line {nb}: connection must contain exactly two zones"
        )

    name1 = parameters[0].strip()
    name2 = parameters[1].strip()

    if not name1 or not name2:
        raise PR(
            f"Line {nb}: connection must contain two valid zones"
        )

    if graph.get_zone(name1) is None:
        raise PR(
            f"Line {nb}: unknown zone '{name1}'"
        )

    if graph.get_zone(name2) is None:
        raise PR(
            f"Line {nb}: unknown zone '{name2}'"
        )

    capacity_str = metadata.get("max_link_capacity", "1")

    try:
        max_link_capacity = int(capacity_str)
    except ValueError:
        raise PR(
            f"Line {nb}: max_link_capacity must be a positive integer"
        )

    if max_link_capacity <= 0:
        raise PR(
            f"Line {nb}: max_link_capacity must be a positive integer"
        )

    graph.add_connection(
        Connection(
            name1=name1,
            name2=name2,
            link_capacity=max_link_capacity
        )
    )


def file_parser(file: str) -> Graph:
    """pareses the file"""
    try:
        with open(file, "r") as f:
            lines = f.readlines()
    except OSError:
        raise PR(f"Error opening file '{file}'")

    drone_line = None
    drone_line_nb = 0

    for number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped and not stripped.startswith("#"):
            drone_line = stripped
            drone_line_nb = number
            break

    if drone_line is None:
        raise PR("Empty file")

    nb_drones = drone_parser(drone_line, drone_line_nb)

    graph = Graph(nb_drones)

    for number, line in enumerate(
        lines[drone_line_nb:],
        start=drone_line_nb + 1
    ):
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if ":" not in stripped:
            raise PR(
                f"Line {number}: missing ':'"
            )

        line_type = stripped.split(":", 1)[0].strip()

        if line_type in ("hub", "start_hub", "end_hub"):
            zone = zone_parser(stripped, number)
            graph.add_zone(zone)

        elif line_type == "connection":
            connection_parser(stripped, number, graph)

        else:
            raise PR(
                f"Line {number}: unrecognized input '{line_type}'"
            )

    graph.validate()

    return graph

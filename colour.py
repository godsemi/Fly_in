from zones import Zone


class Colours:

    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"

    @staticmethod
    def colouring(text: str, colour: str) -> str:
        """Apply an ANSI colour code to a text string."""
        return f"{colour}{text}{Colours.RESET}"

    @staticmethod
    def colour_exit(zone: Zone) -> str:
        """Return a zone name coloured according to its type."""
        type_zone: dict[str, str] = {
            "normal": Colours.WHITE, "priority": Colours.GREEN,
            "blocked": Colours.RED, "restricted": Colours.YELLOW
        }
        colour = type_zone.get(zone.type_zone, Colours.WHITE)
        return Colours.colouring(zone.name, colour)

    @staticmethod
    def drone_colour(id: str) -> str:
        """Return a zone name coloured according to its type."""
        return Colours.colouring(id, Colours.CYAN)

from parser import file_parser
from parse_raise import PR
from simulation import Simulation
import sys


def main():
    """Run the drone simulation from a map file."""
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 main.py <map_file>")
            sys.exit(1)
        graph = file_parser(sys.argv[1])
        sim = Simulation(graph)
        sim.assign_path()
        sim.loop_turn()
        for line in sim.history_movement:
            print(line)
        print(f"Total turns: {len(sim.history_movement)}")
    except PR as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

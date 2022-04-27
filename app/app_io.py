import argparse
from typing import List

def parse_cli_arguments(args: List[str]):
    parser = argparse.ArgumentParser(description='Mela2.0 simulator')
    parser.add_argument('domain_state_file', help='A .json file containing the initial state of the simulation')
    parser.add_argument('control_file', help='Simulation control logic as a .yaml file')
    return parser.parse_args(args)
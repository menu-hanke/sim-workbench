import sys

from sim.operations import operation_lookup
from sim.runners import evaluate_sequence
from sim.generators import compose, generators_from_declaration
from sim.file_io import forest_stands_from_json_file, simulation_declaration_from_yaml_file

if __name__ == "__main__":
    # TODO: use argparse
    try:
        input_filename = sys.argv[1]
        stands = forest_stands_from_json_file(input_filename)
    except:
        stands = []

    simulation_declaration = simulation_declaration_from_yaml_file('control.yaml')

    generators = generators_from_declaration(simulation_declaration, operation_lookup)
    tree = compose(*generators)

    payload = {
        'simulation_state': 200
    }

    chains = tree.operation_chains()

    iteration_counter = 1
    for chain in chains:
        try:
            print("running chain " + str(iteration_counter))
            iteration_counter = iteration_counter + 1
            result = evaluate_sequence(payload, *chain)

            print(result)
        except Exception as e:
            print(e)
        print("\n")

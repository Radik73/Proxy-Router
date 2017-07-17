import argparse

arg_1 = 'version'
arg_2 = 'number_of_port'

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(arg_1)
    parser.add_argument(arg_2)
    return parser
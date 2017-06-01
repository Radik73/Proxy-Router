import argparse

arg_1 = 'number_of_port'

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(arg_1)
    return parser
import argparse
import time


def create_parser():
    arg_1 = 'ip'
    arg_2 = 'number_of_port'
    arg_3 = 'id'
    parser = argparse.ArgumentParser()
    parser.add_argument(arg_1)
    parser.add_argument(arg_2)
    parser.add_argument(arg_3)
    return parser

def work_simulation():
    while True:
        time.sleep(1000)
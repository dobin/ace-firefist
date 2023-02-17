#!/usr/bin/python3

import logging
import argparse

from model import enableOut
from recepies import *

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--recepi', type=int, help='')
    args = parser.parse_args()

    if args.recepi == 1:
        recepi_1()
    elif args.recepi == 2:
        recepi_2()
    elif args.recepi == 3:
        recepi_3()
    else:
        print("Unkown recepi: {}".format(args.recepi))


if __name__ == "__main__":
    enableOut()
    main()

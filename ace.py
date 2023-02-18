#!/usr/bin/python3

import io

import argparse

from model import enableOut
from recipes import *
from log import setupLogging


def main():
    setupLogging()

    parser = argparse.ArgumentParser()
    parser.add_argument('--recipe', type=int, help='')
    args = parser.parse_args()

    if args.recipe == 1:
        recipe_1()
    elif args.recipe == 2:
        recipe_2()
    elif args.recipe == 3:
        recipe_3()
    else:
        print("Unkown recipe: {}".format(args.recipe))


if __name__ == "__main__":
    enableOut()
    main()

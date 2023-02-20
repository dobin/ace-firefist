#!/usr/bin/python3

import io
import os
import importlib

import argparse

from model import *
from recipes import *
from log import setupLogging


def main():
    setupLogging()

    parser = argparse.ArgumentParser()
    parser.add_argument('--recipe', type=str, help='', required=True)
    parser.add_argument('--scan', type=str, help='')
    parser.add_argument('--listenip', type=str, help='')
    parser.add_argument('--listenport', type=int, help='')
    args = parser.parse_args()

    if args.scan:
        enableScanning(args.scan)
    if args.listenip:
        setListenIp(args.listenip)
    if args.listenport:
        setListenPort(args.listenport)

    # From ChatGPT
    recipeMethod = None 
    plugin_files = [f for f in os.listdir('recipes') if f.endswith('.py')]
    for plugin_file in plugin_files:
        if plugin_file == '__init__.py': 
            continue
        module_name = plugin_file[:-3]  # remove the '.py' extension
        module = importlib.import_module('.' + module_name, package='recipes')
        
        if hasattr(module, args.recipe):
            recipeMethod = getattr(module, args.recipe)

    if recipeMethod is None:
        print("Unknown recipe: {}".format(args.recipe))
    else:
        recipeMethod()


if __name__ == "__main__":
    enableOut()
    main()

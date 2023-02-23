#!/usr/bin/python3

import io
import os
import importlib
from typing import List
import argparse

from model import *
from recipes import *
from log import setupLogging
from web import serve
from helpers import *


def contentFilterTest():
    allRoutes: List[AceRoute] = []
    recipeInfos: List[RecipeInfo] = []

    plugin_files = [f for f in os.listdir('recipes') if f.endswith('.py')]
    for plugin_file in plugin_files:
        if plugin_file == '__init__.py': 
            continue
        module_name = plugin_file[:-3]  # remove the '.py' extension
        module = importlib.import_module('.' + module_name, package='recipes')
        
        if hasattr(module, module_name):
            recipeMethod = getattr(module, module_name)

            if recipeMethod is None:
                print("Unknown recipe: {}".format(module_name))
            else:
                logger.info("-[ Make recipe: {}".format(plugin_file))
                routes = recipeMethod()
                allRoutes = allRoutes + routes

                # open its yaml
                recipeInfo = getRecipeInfo("recipes" + "/" + plugin_file + ".yaml", routes)
                if recipeInfo is not None:
                    recipeInfos.append(recipeInfo)


    print(recipeInfos)
    serve(allRoutes, recipeInfos)
        

def startRecipe(recipeName):
    # From ChatGPT
    recipeMethod = None 
    plugin_files = [f for f in os.listdir('recipes') if f.endswith('.py')]
    for plugin_file in plugin_files:
        if plugin_file == '__init__.py': 
            continue
        module_name = plugin_file[:-3]  # remove the '.py' extension
        module = importlib.import_module('.' + module_name, package='recipes')
        
        if hasattr(module, recipeName):
            recipeMethod = getattr(module, recipeName)

    if recipeMethod is None:
        print("Unknown recipe: {}".format(recipeName))
    else:
        routes = recipeMethod()
        serve(routes)


def main():
    enableOut()
    setupLogging()

    parser = argparse.ArgumentParser()
    parser.add_argument('--recipe', type=str, help='', required=True)
    parser.add_argument('--scan', type=str, help='')
    parser.add_argument('--listenip', type=str, help='')
    parser.add_argument('--listenport', type=int, help='')
    parser.add_argument('--templateinfo', action='store_true', help='')
    args = parser.parse_args()

    if args.scan:
        enableScanning(args.scan)
    if args.listenip:
        setListenIp(args.listenip)
    if args.listenport:
        setListenPort(args.listenport)
    if args.templateinfo:
        enableTemplateInfo()

    if args.recipe == "all":
        contentFilterTest()
    else:
        startRecipe(args.recipe)



if __name__ == "__main__":
    main()

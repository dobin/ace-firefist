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


def contentFilterTest(baseUrl):
    allRoutes: List[AceRoute] = []
    recipeInfos: List[RecipeInfo] = []

    recipes = getRecipes()
    for recipe in recipes:
        module_name = recipe[:-3]  # remove the '.py' extension
        module = importlib.import_module('.' + module_name, package='recipes')
        
        if hasattr(module, module_name):
            recipeMethod = getattr(module, module_name)

            if recipeMethod is None:
                print("Unknown recipe: {}".format(module_name))
            else:
                logger.info("-[ Make recipe: {}".format(recipe))
                routes = recipeMethod(baseUrl)
                allRoutes = allRoutes + routes

                # open its yaml
                recipeInfo = getRecipeInfo("recipes" + "/" + recipe + ".yaml", routes)
                if recipeInfo is not None:
                    recipeInfos.append(recipeInfo)


    serve(allRoutes, recipeInfos)
        

def startRecipe(recipeName, baseUrl):
    # From ChatGPT
    recipeMethod = None 
    recipes = getRecipes()
    for recipe in recipes:
        module_name = recipe[:-3]  # remove the '.py' extension
        module = importlib.import_module('.' + module_name, package='recipes.' + module_name)
        if hasattr(module, recipeName):
            recipeMethod = getattr(module, recipeName)

    if recipeMethod is None:
        logging.error("Unknown recipe: {}".format(recipeName))
        logging.error("  Make sure it exists in recipes/")
        logging.error("  Make sure it follows naming standard:")
        logging.error("     recipes/<new>/<new>.py::func <new>()")
    else:
        routes = recipeMethod(baseUrl)
        if len(routes) > 0:
            serve(routes)


def getRecipes():
    res = []
    for d in os.listdir('recipes'):
        plugin_files = [f for f in os.listdir('recipes/' + d) if f.endswith('.py')]
        for plugin_file in plugin_files:
            if plugin_file == '__init__.py': 
                continue
            res.append(plugin_file)
    return res


def main():
    enableOut()
    setupLogging()

    parser = argparse.ArgumentParser()
    parser.add_argument('--recipe', type=str, required=True, help='Which recipe to use ("all" for all)')
    parser.add_argument('--scan', type=str, help='Scan AceFiles with avred-server')
    parser.add_argument('--listenip', type=str, help='IP to listen on')
    parser.add_argument('--listenport', type=int, help='Port to listen on')
    parser.add_argument('--templateinfo', action='store_true', help='Show information about used templates')
    parser.add_argument('--externalurl', type=str, help='External URL of the server (if behind reverse proxy)')
    args = parser.parse_args()

    if args.scan:
        enableScanning(args.scan)
    if args.listenip:
        setListenIp(args.listenip)
    if args.listenport:
        setListenPort(args.listenport)
    if args.templateinfo:
        enableTemplateInfo()

    if args.externalurl:
        baseUrl = args.externalurl
    else:
        baseUrl = "http://{}:{}".format(config.LISTEN_IP, config.LISTEN_PORT)
    logger.info("Using baseUrl: {}".format(baseUrl))
    if args.recipe == "all":
        contentFilterTest(baseUrl)
    else:
        startRecipe(args.recipe, baseUrl)


if __name__ == "__main__":
    main()

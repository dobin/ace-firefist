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
        module = importlib.import_module('.' + module_name, package='recipes.' + module_name)
        if hasattr(module, module_name):
            recipeMethod = getattr(module, module_name)
            if recipeMethod is None:
                print("Unknown recipe: {}".format(module_name))
            else:
                logger.info("-[ Make recipe: {}".format(recipe))
                routes = recipeMethod(baseUrl)
                allRoutes = allRoutes + routes

                # open its yaml
                path = os.path.join("recipes", module_name, recipe + '.yaml')
                recipeInfo = getRecipeInfo(path, routes)
                if recipeInfo is not None:
                    recipeInfos.append(recipeInfo)

    serve(allRoutes, recipeInfos)
        

def startRecipe(recipeName, baseUrl):
    recipeMethod = None
    recipeInfos = []

    recipes = getRecipes()
    for recipe in recipes:
        module_name = recipe[:-3]  # remove the '.py' extension
        module = importlib.import_module('.' + module_name, package='recipes.' + module_name)
        if hasattr(module, recipeName):
            recipeMethod = getattr(module, recipeName)

            # open its yaml
            path = os.path.join("recipes", module_name, recipe + '.yaml')
            recipeInfo = getRecipeInfo(path, [])
            if recipeInfo is not None:
                recipeInfos.append(recipeInfo)

    if recipeMethod is None:
        logging.error("Unknown recipe: {}".format(recipeName))
        logging.error("  Make sure it exists in recipes/")
        logging.error("  Make sure it follows naming standard:")
        logging.error("     recipes/<new>/<new>.py::func <new>()")
    else:
        routes = recipeMethod(baseUrl)
        if len(routes) > 0:
            serve(routes, recipeInfos)


def getRecipes():
    res = []
    for d in os.listdir('recipes'):
        plugin_files = [f for f in os.listdir(os.path.join('recipes', d)) if f.endswith('.py')]
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
    parser.add_argument('--listenip', type=str, required=True, help='IP to listen on')

    parser.add_argument('--scan', type=str, help='Scan AceFiles with avred-server')
    parser.add_argument('--listenport', type=int, help='Port to listen on', default=5000)
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
        if config.LISTEN_IP == "0.0.0.0":
            logging.error("Cant use 0.0.0.0 as listen IP. Please specify a IP.")
            logging.error("Use \"--externalurl http://evil\" to specfiy the URL as seen by the client, if necessary")
            return

        logging.info("Use \"--externalurl http://evil\" to specfiy the URL as seen by the client, if necessary")
        baseUrl = "http://{}:{}".format(config.LISTEN_IP, config.LISTEN_PORT)
    logger.info("Using baseUrl: {}".format(baseUrl))
    if args.recipe == "all":
        contentFilterTest(baseUrl)
    else:
        startRecipe(args.recipe, baseUrl)


if __name__ == "__main__":
    main()

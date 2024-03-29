from flask import Flask, send_file, render_template, send_from_directory
import io
from urllib.parse import urlparse
import os
from typing import List
import glob

import log
from model import *


def serve(routes: List[AceRoute], recipeInfos: List[RecipeInfo]=[]):
    """Start a webserver which serves the `routes`, and additional files like index.html and out/"""
    app = Flask(__name__)

    app.add_url_rule('/', 'index', viewIndex(routes, recipeInfos))
    app.add_url_rule('/out/<filename>', 'out', view_out)

    print("")
    print("Routes:")
    print("  /                      Recipe overview")
    print("  /out/<filename>        out/ files")
    print("  /static/<filename>     static/ files")

    for route in routes:
        if isinstance(route.data, (AceStr, AceBytes)):
            print("  {}   ({})    Download: {} {}".format(route.url, route.data.index, route.download, route.downloadName))
        else:
            print("  {}           Donload: {} {}".format(route.url, route.download, route.downloadName))

        try:
            if route.download:
                app.add_url_rule(route.url, route.url, viewRouteDownload(route))
            else:
                app.add_url_rule(route.url, route.url, viewRoutePlain(route))
        except AssertionError:
            print("Double URL, dropped: {}".format(route.url))
            route.url = route.url + " (doubled, dropped)"


    print("")
    app.run(
        host=config.LISTEN_IP,
        port=config.LISTEN_PORT)


# View for normal (text) files/route
def viewRoutePlain(route):
    def view_func():
        return route.data
    return view_func


# View for downloadable (binary) files/route
def viewRouteDownload(route):
    def view_func():
        # TODO necessary to convert?
        data = route.data
        if isinstance(data, str):
            data = bytes(data, 'utf-8')

        if route.downloadMime is not None:
            ret = send_file(
                io.BytesIO(data),
                as_attachment=True,
                download_name=route.downloadName,
                mimetype=route.downloadMime
            )
            return ret
        else:
            ret = send_file(
                io.BytesIO(data),
                download_name=route.downloadName,
            )
            return ret
    return view_func


# View for the index.html and all its information
def viewIndex(routes, recipeInfos):
    def view_func():
        files = sorted(glob.glob("out/out_*.*"))
        #log = log.GlobalLog.getvalue()
        log = '\n'.join(config.makerCallstack.values())
        return render_template(
            'index.html', 
            files=files,
            routes=routes,
            log=log,
            recipeInfos=recipeInfos)

    return view_func


# View for file in out/ directory
def view_out(filename):
    return send_from_directory('out/', filename, as_attachment=False)

from flask import Flask, send_file, render_template, send_from_directory
import io
from urllib.parse import urlparse
import os
from typing import List
import glob

import log
from model import *


def serve(routes: List[AceRoute]):
    """Start a webserver which serves the `routes`, and additional files like index.html and out/"""
    app = Flask(__name__)

    print("")
    print("Routes:")
    app.add_url_rule('/', 'index', viewIndex(routes))
    app.add_url_rule('/out/<filename>', 'out', view_out)
    print("  /            Recipe overview")

    for route in routes:
        if isinstance(route.data, (AceStr, AceBytes)):
            print("  {}   ({})    Download: {} {}".format(route.url, route.data.index, route.download, route.downloadName))
        else:
            print("  {}           Donload: {} {}".format(route.url, route.download, route.downloadName))

        if route.download:
            app.add_url_rule(route.url, route.url, viewRouteDownload(route))
        else:
            app.add_url_rule(route.url, route.url, viewRoutePlain(route))

    print("")
    app.run()


# View for normal (text) files/route
def viewRoutePlain(route):
    def view_func():
        return route.data
    return view_func


# View for downloadable (binary) files/route
def viewRouteDownload(route):
    def view_func():
        # TODO necessary?
        data = route.data
        if isinstance(data, str):
            data = bytes(data, 'utf-8')
        ret = send_file(
            io.BytesIO(data),
            attachment_filename=route.downloadName,
            # mimetype='image/jpg'
        )
        return ret
    return view_func


# View for the index.html and all its information
def viewIndex(routes):
    def view_func():
        files = sorted(glob.glob("out/out_*.*"))
        return render_template(
            'index.html', 
            files=files,
            routes=routes,
            log=log.GlobalLog.getvalue())

    return view_func


# View for file in out/ directory
def view_out(filename):
    return send_from_directory('out/', filename, as_attachment=False)



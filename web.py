from flask import Flask

# a View which just returns `data`
def serveData(data):
    return f"{data}"


# From ChatGPT
def make_view(view_func, data):
    def view_wrapper(*args, **kwargs):
        return view_func(data, *args, **kwargs)
    return view_wrapper

# Serve the 
def serve(routes):
    app = Flask(__name__)

    for route in routes:
        app.add_url_rule(route.url, view_func=make_view(serveData, route.data))

    app.run()


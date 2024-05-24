from functools import wraps
from flask import request, make_response, current_app, g


def basic_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == current_app.config["SITE_USER"] and auth.password == current_app.config["SITE_PASS"]:
            g.user = auth.username
            return func(*args, **kwargs)
        return make_response("<h1>Access denied<h1>", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return wrapper

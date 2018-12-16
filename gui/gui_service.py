from gui.views import movies, seances, tickets, users, menu
import flask
from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort


from gui.config import current_config

app = flask.Flask(__name__)


@app.before_request
def load_current_user():
    if 'token' in request.cookies:
        g.logged_in = True
        g.user = request.cookies
    else:
        g.user = None
        g.logged_in = False

app.config.from_object(current_config)
app.register_blueprint(movies.mod)
app.register_blueprint(seances.mod)
app.register_blueprint(tickets.mod)
app.register_blueprint(users.mod)
app.register_blueprint(menu.mod)
app.run(port=current_config.PORT)
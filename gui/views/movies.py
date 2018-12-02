from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort

mod = Blueprint('movies', __name__)


@mod.route('/movies/')
def index():
    return render_template("/movies/index.html")


@mod.route('/movies/create')
def create():
    if request.method == 'GET':
        return render_template("/movies/create.html")
    elif request.method == "POST":
        pass
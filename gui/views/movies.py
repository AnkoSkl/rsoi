from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort, Markup
from gui.utils import do_create_movie

mod = Blueprint('movies', __name__)


@mod.route('/movies/')
def index():
    return render_template("/movies/index.html")


@mod.route('/movies/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("/movies/create.html")
    else:
        failed = False
        if 'name' not in request.form or request.form['name']=='':
            flash('Имя не задано')
            failed = True

        if 'description' not in request.form or request.form['description']=='':
            flash('Описание не задано')
            failed = True

        if 'length' not in request.form or request.form['length']=='':
            flash('Длительность не задана')
            failed = True

        if failed:
            return redirect(url_for('movies.create'))

        name = request.form['name']
        description = request.form['description']
        length = request.form['length']
        result = do_create_movie(name, description, length)
        if result.success:
            if result.response.status_code == 201:
                flash(Markup('Фильм успешно добавлен'))
                response = redirect(url_for(result.redirect))
                return response
            else:
                flash(result.response.content.decode('utf-8'))
                return redirect(url_for('movies.create'))
        else:
            flash(result.error)
            return redirect(url_for('movies.create'))


@mod.route('/movies/get')
def get():
    if request.method == 'GET':
        return render_template("/movies/create.html")
    elif request.method == "POST":
        pass


@mod.route('/movies/delete')
def delete():
    if request.method == 'GET':
        return render_template("/movies/create.html")
    elif request.method == "POST":
        pass


@mod.route('/movies/get_all')
def get_all():
    if request.method == 'GET':
        return render_template("/movies/create.html")
    elif request.method == "POST":
        pass
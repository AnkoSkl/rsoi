from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort, Markup
from gui.utils import do_create_movie, do_get_movie, do_delete_movie
import json

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
            flash('Имя не задано', "error")
            failed = True

        if 'description' not in request.form or request.form['description']=='':
            flash('Описание не задано', "error")
            failed = True

        if 'length' not in request.form or request.form['length']=='':
            flash('Длительность не задана', "error")
            failed = True

        if failed:
            return redirect(url_for('movies.create'))

        name = request.form['name']
        description = request.form['description']
        length = request.form['length']
        if not isinstance(length, int):
            flash('Длительность должна быть введена в минутах', 'error')
            return redirect(url_for('movies.create'))
        result = do_create_movie(name, description, length)
        if result.success:
            if result.response.status_code == 201:
                flash('Фильм успешно добавлен', "info")
                response = redirect('movies.create')
                return response
            else:
                flash(result.response.content.decode('utf-8'), "error")
                return redirect(url_for('movies.create'))
        else:
            flash(result.error)
            return redirect(url_for('movies.create'), "error")


@mod.route('/movies/get')
def get():
    if request.method == 'GET':
        if 'movie_id' not in request.args:
            return render_template("/movies/get.html", movie_found=False)
        elif request.args['movie_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('movies.get'))
        else:
            movie_id = request.args["movie_id"]
            result = do_get_movie(movie_id)

            if result.success:
                if result.response.status_code == 200:
                    movie = json.loads(result.response.content)
                    return render_template("/movies/get.html", movie=movie, movie_found=True)
                else:
                    flash("Фильм не найден", "error")
                    return redirect(url_for('movies.get'))
            else:
                flash(result.error, "error")
                return redirect(url_for('movies.get'))


@mod.route('/movies/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        return render_template("/movies/delete.html")
    else:
        if 'movie_id' not in request.form or request.form['movie_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('movies.delete'))
        else:
            movie_id = request.form["movie_id"]
            result = do_delete_movie(movie_id)

            if result.success:
                if result.response.status_code == 204:
                    flash('Фильм успешно удален', "info")
                    response = redirect(url_for('movies.delete'))
                    return response
                else:
                    flash("Фильм не найден", "error")
                    return redirect(url_for('movies.delete'))
            else:
                flash(result.error, "error")
                return redirect(url_for('movies.delete'))


@mod.route('/movies/get_all')
def get_all():
    if request.method == 'GET':
        return render_template("/movies/create.html")
    elif request.method == "POST":
        pass
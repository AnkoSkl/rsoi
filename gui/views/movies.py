from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort, Markup
from gui.utils import do_create_movie, do_get_movie, do_delete_movie, do_get_paginated_movie
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


@mod.route('/movies/get', methods=['GET', 'POST'])
def get():
    if request.method == 'GET':
        return render_template("/movies/get.html", movie_found = False)
    else:
        if 'movie_id' not in request.form or request.form['movie_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('movies.get'))
        else:
            movie_id = request.form["movie_id"]
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


@mod.route('/movies/delete/<movie_id>', methods=['GET', 'POST'])
def delete(movie_id):
    if request.method == 'GET':
        return render_template("/movies/delete.html", movie_id=movie_id)
    else:
        if request.form['submit'] == 'Нет':
            return redirect(url_for('movies.get_all'))
        if request.form['submit'] == 'Да':
            #movie_id = request.args["movie_id"]
            result = do_delete_movie(movie_id)

            if result.success:
                if result.response.status_code == 204:
                    flash('Фильм успешно удален', "info")
                    response = redirect(url_for('movies.get_all'))
                    return response
                else:
                    flash("Фильм не найден", "error")
                    return redirect(url_for('movies.get_all'))
            else:
                flash(result.error, "error")
                return redirect(url_for('movies.get_all'))


@mod.route('/movies/get_all')
def get_all():
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('movies.get_all', page=1))
        if 'submit' in request.form:
            if request.form['submit'] == 'Создать сеанс':
                pass
            if request.form['submit'] == 'Удалить фильм':
                pass
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_movie(page, 10)
        if result.success:
            if result.response.status_code == 200:
                movies_obj = result.response.content
                movies_str = (str(movies_obj)).split('\\n')
                n = len(movies_str)
                movies_str.remove(movies_str[0])
                n = n-1
                movies_str[n-1] = movies_str[n-1][0:-1]
                movies = []
                dictr = json.loads(movies_str[n-1])
                movies_str.remove(movies_str[n-1])
                for movie in movies_str:
                    movie1 = bytes(movie, 'utf8')
                    movies.append(json.loads(movie1))
                return render_template("/movies/get_all.html", movies=movies, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            else:
                flash("Фильм не найден", "error")
                return redirect(url_for('movies.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('movies.index'))
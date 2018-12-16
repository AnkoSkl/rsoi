from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_create_seance, do_get_paginated_seance, do_get_seance
import json

mod = Blueprint('seances', __name__)


@mod.route('/seances/')
def index():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    return render_template("/seances/index.html")


@mod.route('/seances/get/<seance_id>', methods=['GET', 'POST'])
def get(seance_id):
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        result = do_get_seance(seance_id)
        if result.success:
            if result.response.status_code == 200:
                tmp = str(result.response.content)
                list_sm = tmp.split('\\n')
                seance = list_sm[0]
                seance = seance[2:]
                movie = list_sm[1]
                movie = movie[0:-1]
                seance_d = json.loads(seance)
                datetime = str(seance_d["datetime"]).split("_")
                date = datetime[0]
                time = datetime[1]
                dictionary = {"date":date, "time":time}
                ar = seance_d["seats"]
                movie_d = json.loads(movie)
                return render_template("/seances/get.html", seance=seance_d, movie=movie_d, seats = ar,
                                       datetime = dictionary, number_of_seats = len(ar)+1)
            else:
                flash('Ошибка. Фильма или сеанса не существует.', "error")
                return redirect(url_for('seances.get_all'), "error")
        else:
            flash(result.error, "error")
            return redirect(url_for('seances.get_all'), "error")


@mod.route('/seances/create', methods=['GET', 'POST'])
def create():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'movie_id' in request.args:
            movie_id = request.args['movie_id']
            return render_template("/seances/create.html", movie_id=movie_id)
    else:
        failed = False
        if 'number_of_seats' not in request.form or request.form['number_of_seats']=='':
            flash('Количество мест задано', "error")
            failed = True
        try:
            number_of_seats = int(request.form['number_of_seats'])
        except:
            flash('Количество мест должно выражаться числом', 'error')
            return render_template("/seances/create.html", movie_id=request.args['movie_id'])

        if 'date' not in request.form or request.form['date']=='':
            flash('Дата показа фильма не задана', "error")
            failed = True

        if 'time' not in request.form or request.form['time']=='':
            flash('Время начала показа фильма не задано', "error")
            failed = True
        date_time = request.form['date'] + '_' + request.form['time']

        if failed:
            return render_template("/seances/create.html", movie_id=request.args['movie_id'])

        result = do_create_seance(request.args['movie_id'], number_of_seats, date_time)
        if result.success:
            if result.response.status_code == 201:
                flash('Сеанс успешно создан', "info")
                response = redirect('movies/get_all')
                return response
            else:
                st = result.response.content.decode('utf-8')
                if st=='':
                    st = str(result.response.content)
                flash(st, "error")
                return redirect(url_for('movies/get_all'))
        else:
            flash(result.error)
            return redirect(url_for('movies/get_all'), "error")


@mod.route('/seances/get_all')
def get_all():
    if not g.logged_in:
        return redirect(url_for('users.login'))
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('seances.get_all', page=1))
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_seance(page, 10)
        if result.success:
            if result.response.status_code == 200:
                seances_obj = result.response.content
                seances_str = (str(seances_obj)).split('\\n')
                n = len(seances_str)
                seances_str[0] = seances_str[0][2:]
                seances_str[n-1] = seances_str[n-1][0:-1]
                seances = []
                dictr = json.loads(seances_str[n-1])
                seances_str.remove(seances_str[n-1])
                for seance in seances_str:
                    if seance != "":
                        seance1 = json.loads(bytes(seance, 'utf8'))
                        ar = seance1["seats"]
                        number_of_seats = len(ar)
                        number_of_free_seats = 0
                        for item in ar:
                            if item:
                                number_of_free_seats = number_of_free_seats+1
                        datetime = str(seance1["datetime"]).split("_")
                        date = datetime[0]
                        time = datetime[1]
                        dictionary = {"seance_id": seance1["seance_id"], "movie_id": seance1["movie_id"],
                                      "number_of_seats": number_of_seats, "number_of_free_seats": number_of_free_seats,
                                      "date":date, "time":time}
                        seances.append(dictionary)
                return render_template("/seances/get_all.html", seances=seances, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            else:
                flash("Сеансы не найдены", "error")
                return redirect(url_for('seances.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('seances.index'))
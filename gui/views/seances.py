from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_create_seance

mod = Blueprint('seances', __name__)


@mod.route('/seances/')
def index():
    return render_template("/seances/index.html")


@mod.route('/seances/create', methods=['GET', 'POST'])
def create():
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
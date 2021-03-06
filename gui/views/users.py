from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_get_paginated_user, do_get_user
import json

mod = Blueprint('users', __name__)


@mod.route('/users/')
def index():
    return render_template("/users/index.html")


@mod.route('/users/get/<user_id>', methods=['GET', 'POST'])
def get(user_id):
    if request.method == 'GET':
        result = do_get_user(user_id)
        if result.success:
            if result.response.status_code == 200:
                user = json.loads(result.response.content)
                ticket_ids = user['ticket_ids']
                return render_template("/users/get.html", user = user, ticket_ids = ticket_ids)
            else:
                flash('Ошибка. Фильма или сеанса не существует.', "error")
                return redirect(url_for('seances.get_all'), "error")
        else:
            flash(result.error, "error")
            return redirect(url_for('seances.get_all'), "error")


@mod.route('/users/get_all')
def get_all():
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('users.get_all', page=1))
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_user(page, 10)
        if result.success:
            if result.response.status_code == 200:
                users_obj = result.response.content
                users_str = (str(users_obj)).split('\\n')
                n = len(users_str)
                users_str[0] = users_str[0][2:]
                users = []
                users_str[n-1] = users_str[n-1][0:-1]
                dictr = json.loads(users_str[n-1])
                users_str.remove(users_str[n-1])
                for user in users_str:
                    if user != "":
                        user1 = bytes(user, 'utf8')
                        users.append(json.loads(user1))
                return render_template("/users/get_all.html", users=users, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            else:
                flash("Потзователь не найден", "error")
                return redirect(url_for('users.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('users.index'))
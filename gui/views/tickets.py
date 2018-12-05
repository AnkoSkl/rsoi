from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from gui.utils import do_get_paginated_tickets, do_get_ticket
import json

mod = Blueprint('tickets', __name__)


@mod.route('/tickets/')
def index():
    return render_template("/tickets/index.html")


@mod.route('/tickets/get', methods=['GET', 'POST'])
def get():
    if request.method == 'GET':
        return render_template("/tickets/get.html", ticket_found = False)
    else:
        if 'ticket_id' not in request.form or request.form['ticket_id'] == '':
            flash('Идентификатор не задан', "error")
            return redirect(url_for('tickets.get'))
        else:
            ticket_id = request.form["ticket_id"]
            result = do_get_ticket(ticket_id)

            if result.success:
                if result.response.status_code == 200:
                    ticket = json.loads(result.response.content)
                    return render_template("/tickets/get.html", ticket=ticket, ticket_found=True)
                else:
                    flash("Билет не найден", "error")
                    return redirect(url_for('tickets.get'))
            else:
                flash(result.error, "error")
                return redirect(url_for('tickets.get'))


@mod.route('/tickets/buy')
def buy():
    if request.method == 'GET':
        seance_id = request.args['seance_id']
        seat_number = request.args['seat_number']



@mod.route('/tickets/get_all')
def get_all():
    if request.method == 'GET':
        if 'page' not in request.args:
            return redirect(url_for('tickets.get_all', page=1))
        if 'submit' in request.form:
            if request.form['submit'] == 'Создать сеанс':
                pass
            if request.form['submit'] == 'Удалить фильм':
                pass
        page = request.args.get('page', 1, type=int)
        result = do_get_paginated_tickets(page, 10)
        if result.success:
            if result.response.status_code == 200:
                tickets_obj = result.response.content
                tickets_str = (str(tickets_obj)).split('\\n')
                n = len(tickets_str)
                tickets_str[0] = tickets_str[0][2:]
                tickets_str[n-1] = tickets_str[n-1][0:-1]
                tickets = []
                dictr = json.loads(tickets_str[n-1])
                tickets_str.remove(tickets_str[n-1])
                for ticket in tickets_str:
                    if ticket != '':
                        ticket1 = bytes(ticket, 'utf8')
                        tickets.append(json.loads(ticket1))
                return render_template("/tickets/get_all.html", tickets=tickets, prev_url=dictr['is_prev_page'],
                                       next_url=dictr['is_next_page'], next_page=page+1, prev_page=page-1)
            else:
                flash("Билеты не найдены", "error")
                return redirect(url_for('tickets.index'))
        else:
            flash(result.error, "error")
            return redirect(url_for('tickets.index'))
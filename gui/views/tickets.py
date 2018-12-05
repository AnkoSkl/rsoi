from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort

mod = Blueprint('tickets', __name__)


@mod.route('/tickets/')
def index():
    return render_template("/tickets/index.html")


@mod.route('/tickets/get')
def get():
    return render_template("/tickets/get.html")


@mod.route('/tickets/get_all')
def get_all():
    return render_template("/tickets/get_all.html")
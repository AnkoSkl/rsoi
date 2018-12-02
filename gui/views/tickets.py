from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort

mod = Blueprint('tickets', __name__)


@mod.route('/tickets/')
def index():
    return "Hello, World!"
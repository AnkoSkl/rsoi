from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort

mod = Blueprint('seances', __name__)


@mod.route('/seances/')
def index():
    return "Hello, World!"
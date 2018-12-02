from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort

mod = Blueprint('users', __name__)


@mod.route('/users/')
def index():
    return "Hello, World!"
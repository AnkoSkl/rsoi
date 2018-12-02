from gui.views import movies, seances, tickets, users, menu
import flask

app = flask.Flask(__name__)
app.register_blueprint(movies.mod)
app.register_blueprint(seances.mod)
app.register_blueprint(tickets.mod)
app.register_blueprint(users.mod)
app.register_blueprint(menu.mod)

app.run()
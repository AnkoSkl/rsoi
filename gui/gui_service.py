from gui.views import movies, seances, tickets, users, menu
import flask

from gui.config import current_config

app = flask.Flask(__name__)
app.config.from_object(current_config)
app.register_blueprint(movies.mod)
app.register_blueprint(seances.mod)
app.register_blueprint(tickets.mod)
app.register_blueprint(users.mod)
app.register_blueprint(menu.mod)

app.run(port=current_config.PORT)
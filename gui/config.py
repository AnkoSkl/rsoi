class Config(object):
    DEBUG = False
    TESTING = False
    GATEWAY_SERVICE_PATH = "/gateway/api"

    CREATE_PATH = "/create"

    MOVIE_SERVICE_PATH = "/movies"
    MOVIE_URL_PATH = "/<movie_id>"

    SEANCE_SERVICE_PATH = "/seances"
    SEANCE_URL_PATH = "/<seance_id>"

    TICKET_SERVICE_PATH = "/tickets"
    TICKET_URL_PATH = "/<ticket_id>"

    USER_SERVICE_PATH = "/users"
    USER_URL_PATH = "/<user_id>"

    SECRET_KEY = "qwerty1234"

    GET_TOKEN_URL_PATH = "/auth/token"


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5005
    GUI_SERVICE_URL = "http://127.0.0.1:%d" % PORT
    GATEWAY_SERVICE_URL = "http://127.0.0.1:5000"


current_config = DevelopmentConfig()
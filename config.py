class Config(object):
    DEBUG = False
    TESTING = False
    GATEWAY_PATH = "/gateway/api"

    CREATE_PATH = "/create"

    MOVIE_SERVICE_PATH = "/movies"

    SEANCE_SERVICE_PATH = "/seances"

    TICKET_SERVICE_PATH = "/tickets"

    USER_SERVICE_PATH = "/users"

    PORT = 5000
    GATEWAY_URL = "http://127.0.0.1:5000"
    MOVIE_SERVICE_URL = "http://127.0.0.1:5001"
    SEANCE_SERVICE_URL = "http://127.0.0.1:5002"
    TICKET_SERVICE_URL = "http://127.0.0.1:5003"
    USER_SERVICE_URL = "http://127.0.0.1:5004"


current_config = Config()
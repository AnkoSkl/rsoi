from functools import wraps
from flask import g, url_for, flash, abort, request, redirect, make_response
import requests
import requests.exceptions
from gui.config import current_config
import jsonpickle


class Result:
    def __init__(self, success, response=None, error=None, redirect=None):
        self.success = success
        self.error = error
        self.redirect = redirect
        self.response = response


def request_handler(redirect_url):
    def wrap(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                request_result = f(*args, **kwargs)
                return Result(success=True, redirect=redirect_url, response=request_result)
            except requests.exceptions.Timeout as e:
                return Result(success=False, error='Время ожидания ответа превышено. Повторите запрос позже')
            except requests.exceptions.ConnectionError as e:
                return Result(success=False, error='В данный момент сервис недоступен. Повторите запрос позже')
            except requests.exceptions.RequestException as e:
                return Result(success=False, error='Произошла ошибка. Повторите запрос позже')
        return decorated_function
    return wrap


@request_handler(redirect_url='tickets.index')
def do_get_paginated_tickets(page, page_size):
    result = gateway_api_request(current_config.TICKET_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)))
    return result


@request_handler(redirect_url='movies.get_all')
def do_create_seance(movie_id, number_of_seats, date_time):
    result = gateway_api_request(current_config.SEANCE_SERVICE_PATH, 'POST', {'movie_id': movie_id,
                                                                              'datetime': date_time,
                                                                              'number_of_seats': int(number_of_seats)})
    return result


@request_handler(redirect_url='seance.index')
def do_get_paginated_seance(page, page_size):
    result = gateway_api_request(current_config.SEANCE_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)))
    return result


@request_handler(redirect_url='seance.index')
def do_get_seance(seance_id):
    result = gateway_api_request(current_config.SEANCE_SERVICE_PATH+'/'+seance_id, 'GET')
    return result


@request_handler(redirect_url='movies.index')
def do_create_movie(name, description, length):
    result = gateway_api_request(current_config.MOVIE_SERVICE_PATH, 'POST',
                                 {'name': name, 'description': description, 'length': int(length)})
    return result


@request_handler(redirect_url='movies.index')
def do_get_movie(movie_id):
    result = gateway_api_request(current_config.MOVIE_SERVICE_PATH + '/' + movie_id, 'GET')
    return result


@request_handler(redirect_url='movies.index')
def do_get_paginated_movie(page, page_size):
    result = gateway_api_request(current_config.MOVIE_SERVICE_PATH, 'GET',
                                 params=(('page', page), ('page_size', page_size)))
    return result


@request_handler(redirect_url='movies.index')
def do_delete_movie(movie_id):
    result = gateway_api_request(current_config.MOVIE_SERVICE_PATH + '/' + movie_id, 'DELETE')
    return result


def gateway_api_request(service_path, method, data=None, params=None, cookies=None):
    if method == 'GET':
        return requests.get(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                            + service_path, params=params, cookies=cookies)
    elif method == 'POST':
        return requests.post(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                             + service_path + current_config.CREATE_PATH, data=jsonpickle.encode(data), params=params,
                             cookies=cookies)
    elif method == 'PUT':
        return requests.put(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                            + service_path, data, params=params, cookies=cookies)
    elif method == 'DELETE':
        return requests.delete(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                               + service_path, cookies=cookies)
    elif method == 'PATCH':
        return requests.patch(current_config.GATEWAY_SERVICE_URL + current_config.GATEWAY_SERVICE_PATH
                              + service_path, data, cookies=cookies)
    else:
        abort(400)
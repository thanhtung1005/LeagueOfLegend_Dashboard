import json
import logging

import flask as fl


def jsonify(data:dict):
    indent = None
    separators = (',', ':')

    return fl.current_app.response_class(
        (json.dumps(data, indent=indent, separators=separators, cls=json.JSONEncoder), '\n'),
        mimetype=fl.current_app.config['JSONIFY_MIMETYPE']
    )

def badRequest(message="Invalid request."):
    return jsonify({
        'status': False,
        'message': message
    })

def response(data=None, status=True):
    return jsonify({
        'status': status,
        'data':data
   })

def log_err(message=""):
    logging.error(f"{fl.request.path}: {message}")

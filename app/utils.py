import json
import logging

import flask as fl
import pandas as pd


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

def readExcelOrCSVFile(dataFile):
    if dataFile.filename.endswith('.xlsx'):
        result = pd.read_excel(dataFile)
    elif dataFile.filename.endswith('.csv'):
        result = pd.read_csv(dataFile)
    else:
        result = None
    if result is not None:
        result.fillna('', inplace=True)
        result.drop_duplicates(inplace=True)
    return result

def evalData(data) -> list:
    if type(data) != list:
        try:
            data = eval(data)
        except:
            data = []
    return data

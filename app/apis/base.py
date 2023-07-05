import flask as fl
import pandas as pd

from flask import Blueprint

from app import db
from ..utils import (
    badRequest,
    response
)


def createBaseBlueprint(
        blueprintName: str,
        urlPrefix: str,
        dataName: str,
        dbModel: db.Model,
        routes: dict[str, str],
        homePage: str,
        key: str = 'name'
    ) -> Blueprint:

    blueprint = Blueprint(blueprintName, __name__, url_prefix=urlPrefix)

    if 'home' in routes.keys():
        @blueprint.route(routes['home'], methods=['POST', 'GET'])
        def home():
            return fl.render_template(homePage)

    if 'import' in routes.keys():
        @blueprint.route(routes['import'], methods=['POST', 'GET'])
        def importObject():
            if not fl.request.files or 'data_file' not in fl.request.files:
                return badRequest()
            dataFile = fl.request.files.get('data_file')
            if not dataFile:
                return badRequest('Missing params.')

            if dataFile.filename.endswith('.xlsx'):
                df = pd.read_excel(dataFile)
            elif dataFile.filename.endswith('.csv'):
                df = pd.read_csv(dataFile)
            else:
                return badRequest('Invalid file.')

            df.fillna('', inplace=True)
            df.drop_duplicates(inplace=True)
            existedObjects = dbModel.query.all()
            existedKeys = [getattr(object, key) for object in existedObjects]

            invalidData = []
            validData = []
            insertedData = []
            countKeys = df[key].value_counts()
            for row in df.to_dict('records'):
                if row[key] in existedKeys:
                    invalidData.append([row[key], f'{dataName} is existed'])
                elif countKeys[row[key]] > 1:
                    invalidData.append([row[key], f'{dataName} is duplicated'])
                else:
                    validData.append([row[key], f'{dataName} is added'])
                    insertedData.append(row)
            if insertedData:
                queryInserts = dbModel.__table__.insert().values(insertedData)
                db.session.execute(queryInserts)
                db.session.commit()
                insertKey = [data[key] for data in insertedData]
                insertedData = dbModel.query.filter(getattr(dbModel, key).in_(insertKey)).all()
                insertedData = [
                    data.toDict() for data in insertedData
                    if getattr(data, key) in insertKey
                ]
                insertedData = sorted(insertedData, key=lambda x: x[key])
            results = [
                *sorted(invalidData, key=lambda x: x[0]),
                *sorted(validData, key=lambda x: x[0])
            ]
            return response({
                'numAdded': len(validData),
                'numFailed': len(invalidData),
                'added': insertedData,
                'results': results
            })

    if 'getAll' in routes.keys():
        @blueprint.route(routes['getAll'], methods=['POST', 'GET'])
        def getAll():
            allObjects = dbModel.query.all()
            allObjects = sorted(allObjects, key=lambda x: getattr(x, key))
            return response([object.toDict() for object in allObjects])

    if 'getOne' in routes.keys():
        @blueprint.route(f"{routes['getOne']}/<int:id>", methods=['POST', 'GET'])
        def getOne(id):
            object = dbModel.query.get_or_404(id)
            return response(object.toDict())

    if 'delete' in routes.keys():
        @blueprint.route(f"{routes['delete']}/<int:id>", methods=['POST', 'GET'])
        def delete(id):
            objectToDelete = dbModel.query.get_or_404(id)
            try:
                db.session.delete(objectToDelete)
                db.session.commit()
                return response(objectToDelete.toDict())
            except:
                return badRequest(f'There was a problem deleting that {dataName}.')

    if 'update' in routes.keys():
        @blueprint.route(f"{routes['update']}/<int:id>", methods=['POST', 'GET'])
        def update(id):
            objectToUpdate = dbModel.query.get_or_404(id)
            newDataOfObject = fl.request.json
            existedKeys = [
                getattr(object, key) for object in dbModel.query.all()
                if getattr(object, key) != getattr(objectToUpdate, key)
            ]
            if newDataOfObject[key] in existedKeys:
                return badRequest(f"Name {newDataOfObject[key]} is existed.")
            else:
                updatedStatus = {}
                for key, value in newDataOfObject.items():
                    if value.replace('.', '').isnumeric():
                        value = float(value)
                    if getattr(objectToUpdate, key) != value:
                        setattr(objectToUpdate, key, value)
                        updatedStatus[key] = value
                if not updatedStatus:
                    updatedStatus['message'] = 'Nothing to update'
                else:
                    updatedStatus['message'] = f"Successfully update {', '.join(updatedStatus.keys())} of {getattr(objectToUpdate, key)}."
                try:
                    db.session.commit()
                    return response(updatedStatus)
                except:
                    return badRequest(f'There was a problem updating that {dataName}.')

    if 'add' in routes.keys():
        @blueprint.route(routes['add'], methods=['POST', 'GET'])
        def add():
            newObjectData = fl.request.json
            existedKeys = [getattr(object, key) for object in dbModel.query.all()]
            if newObjectData[key] in existedKeys:
                return badRequest(f"Name {newObjectData[key]} is existed.")
            else:
                queryInserts = dbModel.__table__.insert().values([newObjectData])
                db.session.execute(queryInserts)
                db.session.commit()
                allObjects = dbModel.query.all()
                allObjects = sorted(allObjects, key=lambda x: getattr(x, key))
                return response([object.toDict() for object in allObjects])

    if 'search' in routes.keys():
        @blueprint.route(routes['search'], methods=['POST', 'GET'])
        def search():
            allObjects = dbModel.query.all()
            try:
                searchedInfor = fl.request.json
                searchedInfor = searchedInfor.lower()
                searchedObjects = []
                for object in allObjects:
                    if searchedInfor in getattr(object, key).lower():
                        searchedObjects.append(object.toDict())
                return response(searchedObjects)
            except:
                allObjects = sorted(allObjects, key=lambda x: getattr(x, key))
            return response([object.toDict() for object in allObjects])

    if 'getTotal' in routes.keys():
        @blueprint.route(routes['getTotal'], methods=['POST', 'GET'])
        def getTotal():
            allObjects = dbModel.query.all()
            return response(len(allObjects))

    return blueprint

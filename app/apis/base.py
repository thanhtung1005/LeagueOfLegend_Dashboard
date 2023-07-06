import flask as fl
import pandas as pd

from flask import Blueprint

from app import db
from ..utils import (
    badRequest,
    response
)


class BaseBlueprint():

    def __init__(
            self,
            blueprintName: str,
            urlPrefix: str,
            dataName: str,
            dbModel: db.Model,
            routes: dict[str, str],
            homePage: str,
            key: str = 'name'
        ):

        self.blueprint = Blueprint(blueprintName, __name__, url_prefix=urlPrefix)
        self.dataName = dataName
        self.dbModel = dbModel
        self.routes = routes
        self.homePage = homePage
        self.key = key

        self.createRoutes()

    def createRoutes(self):
        if 'home' in self.routes:
            self.createHomeRoute()
        if 'import' in self.routes:
            self.createImportRoute()
        if 'getAll' in self.routes:
            self.createGetAllRoute()
        if 'getOne' in self.routes:
            self.createGetOneRoute()
        if 'delete' in self.routes:
            self.createDeleteRoute()
        if 'update' in self.routes:
            self.createUpdateRoute()
        if 'add' in self.routes:
            self.createAddRoute()
        if 'search' in self.routes:
            self.createSearchRoute()
        if 'getTotal' in self.routes:
            self.createGetTotalRoute()

    def createHomeRoute(self):
        @self.blueprint.route(self.routes['home'], methods=['POST', 'GET'])
        def home():
            return fl.render_template(self.homePage)

    def createImportRoute(self):
        @self.blueprint.route(self.routes['import'], methods=['POST', 'GET'])
        def importObject():
            if not fl.request.files or 'importFile' not in fl.request.files:
                return badRequest()
            dataFile = fl.request.files.get('importFile')
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
            existedObjects = self.dbModel.query.all()
            existedKeys = [getattr(object, self.key) for object in existedObjects]

            invalidData = []
            validData = []
            insertedData = []
            countKeys = df[self.key].value_counts()
            for row in df.to_dict('records'):
                if row[self.key] in existedKeys:
                    invalidData.append([row[self.key], f'{self.dataName} is existed'])
                elif countKeys[row[self.key]] > 1:
                    invalidData.append([row[self.key], f'{self.dataName} is duplicated'])
                else:
                    validData.append([row[self.key], f'{self.dataName} is added'])
                    insertedData.append(row)
            if insertedData:
                queryInserts = self.dbModel.__table__.insert().values(insertedData)
                db.session.execute(queryInserts)
                db.session.commit()
                insertKey = [data[self.key] for data in insertedData]
                insertedData = self.dbModel.query.filter(getattr(self.dbModel, self.key).in_(insertKey)).all()
                insertedData = [
                    data.toDict() for data in insertedData
                    if getattr(data, self.key) in insertKey
                ]
                insertedData = sorted(insertedData, key=lambda x: x[self.key])
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

    def createGetAllRoute(self):
        @self.blueprint.route(self.routes['getAll'], methods=['POST', 'GET'])
        def getAll():
            allObjects = self.dbModel.query.all()
            allObjects = sorted(allObjects, key=lambda x: getattr(x, self.key))
            return response([object.toDict() for object in allObjects])

    def createGetOneRoute(self):
        @self.blueprint.route(f"{self.routes['getOne']}/<int:id>", methods=['POST', 'GET'])
        def getOne(id):
            object = self.dbModel.query.get_or_404(id)
            return response(object.toDict())

    def createDeleteRoute(self):
        @self.blueprint.route(f"{self.routes['delete']}/<int:id>", methods=['POST', 'GET'])
        def delete(id):
            objectToDelete = self.dbModel.query.get_or_404(id)
            try:
                db.session.delete(objectToDelete)
                db.session.commit()
                return response(objectToDelete.toDict())
            except:
                return badRequest(f'There was a problem deleting that {self.dataName}.')

    def createUpdateRoute(self):
        @self.blueprint.route(f"{self.routes['update']}/<int:id>", methods=['POST', 'GET'])
        def update(id):
            objectToUpdate = self.dbModel.query.get_or_404(id)
            newDataOfObject = fl.request.json
            existedKeys = [
                getattr(object, key) for object in self.dbModel.query.all()
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
                    return badRequest(f'There was a problem updating that {self.dataName}.')

    def createAddRoute(self):
        @self.blueprint.route(self.routes['add'], methods=['POST', 'GET'])
        def add():
            newObjectData = fl.request.json
            existedKeys = [getattr(object, self.key) for object in self.dbModel.query.all()]
            if newObjectData[self.key] in existedKeys:
                return badRequest(f"Name {newObjectData[self.key]} is existed.")
            else:
                queryInserts = self.dbModel.__table__.insert().values([newObjectData])
                db.session.execute(queryInserts)
                db.session.commit()
                allObjects = self.dbModel.query.all()
                allObjects = sorted(allObjects, key=lambda x: getattr(x, self.key))
                return response([object.toDict() for object in allObjects])

    def createSearchRoute(self):
        @self.blueprint.route(self.routes['search'], methods=['POST', 'GET'])
        def search():
            allObjects = self.dbModel.query.all()
            try:
                searchedInfor = fl.request.json
                searchedInfor = searchedInfor.lower()
                searchedObjects = []
                for object in allObjects:
                    if searchedInfor in getattr(object, self.key).lower():
                        searchedObjects.append(object.toDict())
                return response(searchedObjects)
            except:
                allObjects = sorted(allObjects, key=lambda x: getattr(x, self.key))
            return response([object.toDict() for object in allObjects])

    def createGetTotalRoute(self):
        @self.blueprint.route(self.routes['getTotal'], methods=['POST', 'GET'])
        def getTotal():
            allObjects = self.dbModel.query.all()
            return response(len(allObjects))

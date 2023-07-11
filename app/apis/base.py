import flask as fl
import pandas as pd

from flask import Blueprint

from app import db
from .routes import Route
from ..utils import (
    badRequest,
    response,
    readExcelOrCSVFile
)


class BaseBlueprint():

    def __init__(self,
            blueprintName: str,
            urlPrefix: str,
            dataName: str,
            routes: dict[str, str],
            homePage: str,
            key: str = 'name'
        ):

        self.blueprint = Blueprint(blueprintName, __name__, url_prefix=urlPrefix)
        self.dataName = dataName
        self.routes = routes
        self.homePage = homePage
        self.key = key

        # self.createRoutes()

    def createRoutes(self, dbModel: db.Model):
        if Route.Home in self.routes:
            self.createHomeRoute()
        if Route.Import in self.routes:
            self.createImportRoute(dbModel)
        if Route.GetAll in self.routes:
            self.createGetAllRoute(dbModel)
        if Route.Get in self.routes:
            self.createGetRoute(dbModel)
        if Route.Delete in self.routes:
            self.createDeleteRoute(dbModel)
        if Route.Update in self.routes:
            self.createUpdateRoute(dbModel)
        if Route.Add in self.routes:
            self.createAddRoute(dbModel)
        if Route.Search in self.routes:
            self.createSearchRoute(dbModel)
        if Route.GetTotal in self.routes:
            self.createGetTotalRoute(dbModel)
        return None

    def createHomeRoute(self):
        @self.blueprint.route(self.routes[Route.Home], methods=['POST', 'GET'])
        def home():
            return fl.render_template(self.homePage)

    def createDeleteAllRoute(self, dbModels: list[db.Model]):
        @self.blueprint.route(self.routes[Route.DeleteAll], methods=['POST', 'GET'])
        def deleteAllObject():
            for dbModel in dbModels:
                try:
                    dbModel.query.delete()
                    db.session.commit()
                except:
                    return badRequest(f'There was a problem when delele all {self.dataName}')
            return response(f'Successfully delete all {self.dataName}')

    def createImportRoute(self, dbModel: db.Model):
        @self.blueprint.route(self.routes[Route.Import], methods=['POST', 'GET'])
        def importObject():
            if not fl.request.files or 'importFile' not in fl.request.files:
                return badRequest()
            dataFile = fl.request.files.get('importFile')
            if not dataFile:
                return badRequest('Missing params.')

            df = readExcelOrCSVFile(dataFile)
            if df is None:
                return badRequest('Invalid file.')
            # NOTE: need verify data here
            result = self.importToDatabase(df, dbModel)
            return response(result)

    def importToDatabase(self, df: pd.DataFrame, dbModel: db.Model):
        existedObjects = dbModel.query.all()
        existedKeys = [getattr(object, self.key) for object in existedObjects]
        invalidData, validData, insertedData = [], [], []
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
            queryInserts = dbModel.__table__.insert().values(insertedData)
            db.session.execute(queryInserts)
            db.session.commit()
        allObjects = dbModel.query.all()
        allObjects = sorted(allObjects, key=lambda x: getattr(x, self.key))
        results = [
            *sorted(invalidData, key=lambda x: x[0]),
            *sorted(validData, key=lambda x: x[0])
        ]
        return {
            'numAdded': len(validData),
            'numFailed': len(invalidData),
            'objectsList': [object.toDict() for object in allObjects],
            'results': results
        }

    def createGetAllRoute(self, dbModel: db.Model):
        @self.blueprint.route(self.routes[Route.GetAll], methods=['POST', 'GET'])
        def getAll():
            result = self.getAllObjects(dbModel)
            return response(result)

    def getAllObjects(self, dbModel: db.Model):
        allObjects = dbModel.query.all()
        allObjects = sorted(allObjects, key=lambda x: getattr(x, self.key))
        return [object.toDict() for object in allObjects]

    def createGetRoute(self, dbModel: db.Model):
        @self.blueprint.route(f"{self.routes[Route.Get]}/<int:id>", methods=['POST', 'GET'])
        def getOne(id: int):
            result = self.getObject(id, dbModel)
            return response(result)

    def getObject(self, id: int, dbModel: db.Model):
        object = dbModel.query.get_or_404(id)
        return object.toDict()

    def createDeleteRoute(self, dbModel: db.Model):
        @self.blueprint.route(f"{self.routes[Route.Delete]}/<int:id>", methods=['POST', 'GET'])
        def delete(id):
            result = self.deleteObject(id, dbModel)
            if result is None:
                return badRequest(f'There was a problem deleting that {self.dataName}.')
            return response(result)

    def deleteObject(self, id: int, dbModel: db.Model):
        objectToDelete = dbModel.query.get_or_404(id)
        try:
            db.session.delete(objectToDelete)
            db.session.commit()
            return objectToDelete.toDict()
        except:
            return None

    def createUpdateRoute(self, dbModel: db.Model):
        @self.blueprint.route(f"{self.routes[Route.Update]}/<int:id>", methods=['POST', 'GET'])
        def update(id):
            objectToUpdate = dbModel.query.get_or_404(id)
            newDataOfObject = fl.request.json
            existedKeys = [
                getattr(object, self.key) for object in dbModel.query.all()
                if getattr(object, self.key) != getattr(objectToUpdate, self.key)
            ]
            if newDataOfObject[self.key] in existedKeys:
                return badRequest(f"Name {newDataOfObject[self.key]} is existed.")
            else:
                result = self.updateObject(objectToUpdate, newDataOfObject)
                if result is None:
                    return badRequest(f'There was a problem updating that {self.dataName}.')
                return response(result)

    def updateObject(self, objectToUpdate, newDataOfObject):
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
            updatedStatus['id'] = objectToUpdate.id
            updatedStatus['message'] = f"Successfully update {', '.join(updatedStatus.keys())} of {getattr(objectToUpdate, self.key)}."
        try:
            db.session.commit()
            return updatedStatus
        except:
            return None

    def createAddRoute(self, dbModel: db.Model):
        @self.blueprint.route(self.routes[Route.Add], methods=['POST', 'GET'])
        def add():
            newObjectData = fl.request.json
            existedKeys = [getattr(object, self.key) for object in dbModel.query.all()]
            if newObjectData[self.key] in existedKeys:
                return badRequest(f"Name {newObjectData[self.key]} is existed.")
            else:
                result = self.addObject()
                return response(result)

    def addObject(self, newObjectData: dict, dbModel: db.Model):
        queryInserts = dbModel.__table__.insert().values([newObjectData])
        db.session.execute(queryInserts)
        db.session.commit()
        allObjects = dbModel.query.all()
        allObjects = sorted(allObjects, key=lambda x: getattr(x, self.key))
        return [object.toDict() for object in allObjects]

    def createSearchRoute(self, dbModel: db.Model):
        @self.blueprint.route(self.routes[Route.Search], methods=['POST', 'GET'])
        def search():
            result = self.searchObject()
            return response(result)

    def searchObject(self, dbModel: db.Model):
        allObjects = dbModel.query.all()
        try:
            searchedInfor = fl.request.json
            searchedInfor = searchedInfor.lower()
            searchedObjects = []
            for object in allObjects:
                if searchedInfor in getattr(object, self.key).lower():
                    searchedObjects.append(object)
        except:
            searchedObjects = sorted(allObjects, key=lambda x: getattr(x, self.key))
        return [object.toDict() for object in searchedObjects]

    def createGetTotalRoute(self, dbModel: db.Model):
        @self.blueprint.route(self.routes[Route.GetTotal], methods=['POST', 'GET'])
        def getTotal():
            allObjects = dbModel.query.all()
            return response(len(allObjects))

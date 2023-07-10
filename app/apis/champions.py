import pandas as pd

from app import db
from .base import BaseBlueprint
from .routes import Route
from ..models import (
    Champion,
    ChampionClass,
    ChampionRole,
    Class,
    Role
)
from ..utils import (
    evalData,
    response
)


routes = {
    Route.Add: '/addChampion',
    Route.Delete: '/deleteChampion',
    Route.DeleteAll: '/deleteAllChampions',
    Route.GetAll: '/getAllChampions',
    Route.Get: '/getChampion',
    Route.Home: '/',
    Route.Import: '/importChampions',
    Route.Search: '/searchChampion',
    Route.Update: '/updateChampion',
}


class ChampionsBlueprint(BaseBlueprint):

    def __init__(self):
        super().__init__(
            blueprintName='champions',
            urlPrefix='/champions',
            dataName='champion',
            routes=routes,
            homePage='pages/champions.html',
            key='name'
        )

    def createGetAllChampionsInforRoute(self):
        @self.blueprint.route('/getAllChampionsInfor', methods=['GET', 'POST'])
        def getAllChampionsInfor():
            allChampions = Champion.query.all()
            data = {
                attr: [getattr(champion, attr) for champion in allChampions]
                for attr in ['name', 'infoAttack', 'infoMagic', 'infoDefense', 'infoDifficulty']
            }
            data['total'] = len(data['name'])
            return response(data)

    def getAllObjects(self, dbModel: db.Model):
        championsList = []
        for champion in dbModel.query.all():
            championDict = champion.toDict()
            classes = ChampionClass.query.filter(ChampionClass.championId == champion.id).all()
            classes = set([
                Class.query.get_or_404(championClass.classId).name
                for championClass in classes
            ])
            roles = ChampionRole.query.filter(ChampionRole.championId == champion.id).all()
            roles = set([
                Role.query.get_or_404(role.roleId).name
                for role in roles
            ])
            championDict['classes'] = ', '.join(classes)
            championDict['roles'] = ', '.join(roles)
            championsList.append(championDict)
        championsList = sorted(championsList, key=lambda x: x['name'])
        return championsList

    def importToDatabase(self, df: pd.DataFrame, dbModel: db.Model):
        existedChampions = dbModel.query.all()
        existedChampionKeys = [getattr(object, self.key) for object in existedChampions]
        classNames = [championClass.name for championClass in Class.query.all()]
        roleNames = [role.name for role in Role.query.all()]
        invalidData, validData, insertedChampions = [], [], []
        countKeys = df[self.key].value_counts()
        insertedChampionClass = []
        insertedChampionRole =[]
        for row in df.to_dict('records'):
            if row[self.key] in existedChampionKeys:
                invalidData.append([row[self.key], f'{self.dataName} is existed'])
            elif countKeys[row[self.key]] > 1:
                invalidData.append([row[self.key], f'{self.dataName} is duplicated'])
            else:
                validData.append([row[self.key], f'{self.dataName} is added'])
                row['classes'] = evalData(row['classes'])
                for className in row['classes']:
                    if className in classNames:
                        insertedChampionClass.append((row[self.key], className))
                row['roles'] = evalData(row['roles'])
                for roleName in row['roles']:
                    if roleName in roleNames:
                        insertedChampionRole.append((row[self.key], roleName))
                row.pop('classes')
                row.pop('roles')
                insertedChampions.append(row)
        if insertedChampions:
            queryInsertedChampions = dbModel.__table__.insert().values(insertedChampions)
            db.session.execute(queryInsertedChampions)
            db.session.commit()
            self.insertChampionClassRole(insertedChampionClass, insertedChampionRole)
        allObjects = self.getAllObjects(dbModel)
        results = [
            *sorted(invalidData, key=lambda x: x[0]),
            *sorted(validData, key=lambda x: x[0])
        ]
        return {
            'numAdded': len(validData),
            'numFailed': len(invalidData),
            'objectsList': allObjects,
            'results': results
        }

    def insertChampionClassRole(self, insertedChampionClass: list, insertedChampionRole: list) -> None:
        insertedChampionClass = [
            {
                'championId': Champion.query.filter(Champion.name == championName).first().id,
                'classId': Class.query.filter(Class.name == className).first().id,
            }
            for championName, className in insertedChampionClass
        ]
        insertedChampionRole = [
            {
                'championId': Champion.query.filter(Champion.name == championName).first().id,
                'roleId': Role.query.filter(Role.name == roleName).first().id,
            }
            for championName, roleName in insertedChampionRole
        ]
        if insertedChampionClass:
            queryInsertedChampionClass = ChampionClass.__table__.insert().values(insertedChampionClass)
            db.session.execute(queryInsertedChampionClass)
            db.session.commit()
        if insertedChampionRole:
            queryInsertedChampionRole = ChampionRole.__table__.insert().values(insertedChampionRole)
            db.session.execute(queryInsertedChampionRole)
            db.session.commit()

        return None

championsBlueprint = ChampionsBlueprint()
championsBlueprint.createRoutes(Champion)
championsBlueprint.createDeleteAllRoute([ChampionRole, ChampionClass, Champion])
championsBlueprint.createGetAllChampionsInforRoute()

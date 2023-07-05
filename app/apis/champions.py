from .base import createBaseBlueprint
from ..models import Champion
from ..utils import (
    badRequest,
    response
)


routes = {
    'add': '/addChampion',
    'delete': '/deleteChampion',
    'getAll': '/getAllChampions',
    'getOne': '/getChampion',
    'home': '/',
    'import': '/importChampions',
    'search': '/searchChampion',
    'update': '/updateChampion',
}

championsBlueprint = createBaseBlueprint(
    blueprintName='champions',
    urlPrefix='/champions',
    dataName='champion',
    dbModel=Champion,
    routes=routes,
    homePage='pages/champions.html'
)

@championsBlueprint.route('getAllChampionsInfor', methods=['GET', 'POST'])
def getAllChampionsInfor():
    allChampions = Champion.query.all()
    data = {
        attr: [getattr(champion, attr) for champion in allChampions]
        for attr in ['name', 'infoAttack', 'infoMagic', 'infoDefense', 'infoDifficulty']
    }
    data['total'] = len(data['name'])
    return response(data)

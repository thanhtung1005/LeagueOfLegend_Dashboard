from .base import createBaseBlueprint
from ..models import Item
from ..utils import (
    badRequest,
    response
)


routes = {
    'add': '/addItem',
    'delete': '/deleteItem',
    'getAll': '/getAllItems',
    'getOne': '/getItem',
    'home': '/',
    'import': '/importItems',
    'search': '/searchItem',
    'update': '/updateItem',
}

itemsBlueprint = createBaseBlueprint(
    blueprintName='items',
    urlPrefix='/items',
    dataName='item',
    dbModel=Item,
    routes=routes,
    homePage='pages/items.html',
)

@itemsBlueprint.route('/getAllItemsPrice', methods=['GET', 'POST'])
def getAllItemsPrice():
    allItems = Item.query.all()
    data = {
        attr: [getattr(item, attr) for item in allItems]
        for attr in ['name', 'buyPrice', 'sellPrice']
    }
    data['total'] = len(data['name'])

    if data['total']:
        data['mostExpensive'] = max(data['buyPrice'])
        data['maxLoss'] = max([
            data['buyPrice'][i] - data['sellPrice'][i]
            for i in range(data['total'])
        ])
    else:
        data['mostExpensive'] = 0
        data['maxLoss'] = 0
    return response(data)

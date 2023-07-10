from .base import BaseBlueprint
from .routes import Route
from ..models import Item
from ..utils import (
    badRequest,
    response
)


routes = {
    Route.Add: '/addItem',
    Route.Delete: '/deleteItem',
    Route.DeleteAll: '/deleteAllItems',
    Route.GetAll: '/getAllItems',
    Route.Get: '/getItem',
    Route.Home: '/',
    Route.Import: '/importItems',
    Route.Search: '/searchItem',
    Route.Update: '/updateItem',
}

itemsBlueprint = BaseBlueprint(
    blueprintName='items',
    urlPrefix='/items',
    dataName='item',
    routes=routes,
    homePage='pages/items.html',
    key='name'
)
itemsBlueprint.createRoutes(Item)
itemsBlueprint.createDeleteAllRoute([Item])

@itemsBlueprint.blueprint.route('/getAllItemsPrice', methods=['GET', 'POST'])
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

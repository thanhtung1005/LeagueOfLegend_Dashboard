from .base import BaseBlueprint
from .routes import Route
from ..models import (
    ChampionClass,
    Class
)
from ..utils import (
    badRequest,
    response
)


routes = {
    Route.Add: '/addClass',
    Route.Delete: '/deleteClass',
    Route.DeleteAll: '/deleteAllClasses',
    Route.GetAll: '/getAllClasses',
    Route.Get: 'getClass',
    Route.Home: '/',
    Route.Import: '/importClasses',
    Route.Search: '/searchClass',
    Route.GetTotal: '/getTotalClasses',
    Route.Update: '/updateClass'
}

classesBlueprint = BaseBlueprint(
    blueprintName='classes',
    urlPrefix='/classes',
    dataName='class',
    routes=routes,
    homePage='pages/classes.html',
    key='name'
)
classesBlueprint.createRoutes(Class)
classesBlueprint.createDeleteAllRoute([ChampionClass, Class])

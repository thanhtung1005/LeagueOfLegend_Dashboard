from .base import createBaseBlueprint
from ..models import Class
from ..utils import (
    badRequest,
    response
)


routes = {
    'add': '/addClass',
    'delete': '/deleteClass',
    'getAll': '/getAllClasses',
    'home': '/',
    'import': '/importClasses',
    'search': '/searchClass',
    'getTotal': '/getTotalClasses'
}

classesBlueprint = createBaseBlueprint(
    blueprintName='classes',
    urlPrefix='/classes',
    dataName='class',
    dbModel=Class,
    routes=routes,
    homePage='pages/Classes.html'
)

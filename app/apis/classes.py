from .base import BaseBlueprint
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

classesBlueprint = BaseBlueprint(
    blueprintName='classes',
    urlPrefix='/classes',
    dataName='class',
    dbModel=Class,
    routes=routes,
    homePage='pages/Classes.html'
)

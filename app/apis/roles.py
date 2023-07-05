from .base import createBaseBlueprint
from ..models import Role
from ..utils import (
    badRequest,
    response
)


routes = {
    'add': '/addRole',
    'delete': '/deleteRole',
    'getAll': '/getAllRoles',
    'home': '/',
    'import': '/importRoles',
    'search': '/searchRole',
    'getTotal': '/getTotalRoles'
}

rolesBlueprint = createBaseBlueprint(
    blueprintName='roles',
    urlPrefix='/roles',
    dataName='role',
    dbModel=Role,
    routes=routes,
    homePage='pages/roles.html'
)

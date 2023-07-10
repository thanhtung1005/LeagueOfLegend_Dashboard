from .base import BaseBlueprint
from .routes import Route
from ..models import (
    ChampionRole,
    Role
)
from ..utils import (
    badRequest,
    response
)


routes = {
    Route.Add: '/addRole',
    Route.Delete: '/deleteRole',
    Route.DeleteAll: '/deleteAllRoles',
    Route.GetAll: '/getAllRoles',
    Route.Get: '/getRole',
    Route.Home: '/',
    Route.Import: '/importRoles',
    Route.Search: '/searchRole',
    Route.GetTotal: '/getTotalRoles',
    Route.Update: '/updateRole'
}

rolesBlueprint = BaseBlueprint(
    blueprintName='roles',
    urlPrefix='/roles',
    dataName='role',
    routes=routes,
    homePage='pages/roles.html',
    key='name'
)
rolesBlueprint.createRoutes(Role)
rolesBlueprint.createDeleteAllRoute([ChampionRole, Role])

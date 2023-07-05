from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from .config import config

db = SQLAlchemy()
compress = Compress()

def createApp():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    compress.init_app(app)
    from app.apis import (
        homeBlueprint,
        championsBlueprint,
        itemsBlueprint,
        classesBlueprint,
        rolesBlueprint
    )
    app.register_blueprint(homeBlueprint)
    app.register_blueprint(championsBlueprint)
    app.register_blueprint(itemsBlueprint)
    app.register_blueprint(classesBlueprint)
    app.register_blueprint(rolesBlueprint)

    return app

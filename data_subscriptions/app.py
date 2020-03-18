from flask import Flask

from data_subscriptions import api
from data_subscriptions.extensions import db, migrate


def create_app(testing=False, cli=False):
    app = Flask("data_subscriptions")
    app.config.from_object("data_subscriptions.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app, cli)
    register_blueprints(app)

    return app


def configure_extensions(app, cli):
    db.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)

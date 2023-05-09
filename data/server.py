from flask import Flask

from data.views.index import index_blueprint
from data.views.choose_page import choose_blueprint
from data.views.game import fight_blueprint
from data.views.game import hit_blueprint
from data.views.game import skill_blueprint
from data.views.game import pass_blueprint
from data.views.game import end_blueprint


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    app.register_blueprint(index_blueprint)
    app.register_blueprint(choose_blueprint)
    app.register_blueprint(fight_blueprint)
    app.register_blueprint(hit_blueprint)
    app.register_blueprint(skill_blueprint)
    app.register_blueprint(pass_blueprint)
    app.register_blueprint(end_blueprint)

    return app

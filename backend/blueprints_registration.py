from quart import Quart
from app.api.assistant_manager.blueprint import assistant_blueprint


def register_blueprints(app: Quart) -> None:
    app.register_blueprint(assistant_blueprint, url_prefix="/assistant")

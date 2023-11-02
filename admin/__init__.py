import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "pitg.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from . import auth
    from . import api
    from . import mangrove

    app.register_blueprint(auth.bp)

    app.register_blueprint(mangrove.bp)
    app.add_url_rule("/", endpoint="index")

    app.register_blueprint(api.bp)

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app

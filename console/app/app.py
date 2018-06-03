# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_moment import Moment
from flask_mail import Mail
from flask_uploads import UploadSet, configure_uploads, patch_request_class, AUDIO, ALL

from config import Config
from .assets import assets_env, bundles
from .error_handle import Ehandle
from .jinja_env import JinjaEnv
from .base_model import BaseModel

bootstrap = Bootstrap()
db = SQLAlchemy(model_class=BaseModel)
babel = Babel()
moment = Moment()
mail = Mail()

error_handle = Ehandle()
jinja_env = JinjaEnv()
upload_video = UploadSet('videos', ALL)

login_manager = LoginManager()
# login_manager.session_protection = 'strong'
# message in warning, error, success
# login_manager.login_message = {'info': "您还未登录"}
# login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Config.init_app(app)

    jinja_env.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    assets_env.init_app(app)
    assets_env.register(bundles)
    error_handle.init_app(app)

    configure_uploads(app, upload_video)
    patch_request_class(app, size=640 * 1024 * 1024)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 公共模板
    from .temps import temps as temps_blueprint
    app.register_blueprint(temps_blueprint, url_prefix='/temps')

    # 管理
    from .manage import manage as manage_blueprint
    app.register_blueprint(manage_blueprint, url_prefix='/manage')

    # 帮助
    from .help import help as help_blueprint
    app.register_blueprint(help_blueprint, url_prefix='/help')

    # 联系方式
    from .contact import contact as contact_blueprint
    app.register_blueprint(contact_blueprint, url_prefix='/contact')

    return app

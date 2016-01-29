from flask import Flask
from sqlalchemy import create_engine
from flask.ext.login import LoginManager
from sqlalchemy.orm import sessionmaker
from .config import DevelopmentConfig as app_config
from flask.ext.seasurf import SeaSurf
from models import Base
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore
from sqlalchemy_imageattach.context import (pop_store_context,
                                            push_store_context)

app = Flask(__name__)
app.config.from_object(app_config)
csrf = SeaSurf()
csrf.init_app(app)
fs_store = HttpExposedFileSystemStore('app/static', 'images/')
app.wsgi_app = fs_store.wsgi_middleware(app.wsgi_app)

engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

login_manager = LoginManager()
login_manager.init_app(app)

# Set the storage context for the images
# http://sqlalchemy-imageattach.readthedocs.org/en/0.9.0/guide/context.html#implicit-contexts


@app.before_request
def start_implicit_store_context():
    push_store_context(fs_store)


@app.teardown_request
def stop_implicit_store_context(exception=None):
    pop_store_context()

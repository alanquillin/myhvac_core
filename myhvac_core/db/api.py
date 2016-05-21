from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from myhvac_core import cfg
from myhvac_core.db import models
from myhvac_core.db.measurements import *
from myhvac_core.db.rooms import *
from myhvac_core.db.sensors import *

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('connection_string', required=True,
                help='Database connection string.  Ex: mysql://user:pass@localhost:port/database')
]
CONF = cfg.CONF
CONF.register_opts(opts, 'db')

engine = None
Session = None


def init_db():
    global engine, Session

    LOG.debug('Database connection string: %s', CONF.db.connection_string)

    engine = create_engine(CONF.db.connection_string)
    Session = sessionmaker()
    Session.configure(bind=engine)

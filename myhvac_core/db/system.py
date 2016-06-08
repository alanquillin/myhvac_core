from myhvac_core.db import models
from myhvac_core.db import programs

from datetime import datetime
import logging

LOG = logging.getLogger(__name__)


def get_current_system_config(session):
    return session.query(models.SystemConfig)\
        .filter_by(active=True)\
        .order_by(models.SystemConfig.timestamp.desc())\
        .first()


def set_program(session, program_name=None, program_id=None):
    if not program_id:
        if not program_name:
            raise Exception('Trying to set program, but no name or id were provided')
        program_id = programs.get_program_by_name(session, program_name)

    update_config(session, current_program_id=program_id)


def update_config(session, **data):
    curr_config = get_current_system_config(session)

    curr_config.active = 0

    config = models.SystemConfig(timedate=datetime.now(), active=True)

    config.current_program_id = data.get('current_program_id', curr_config.current_program_id)

    session.add(config)
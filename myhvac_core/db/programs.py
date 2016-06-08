from myhvac_core.db import models

import logging

LOG = logging.getLogger(__name__)


def _get_programs(session, **kwargs):
    return session.query(models.Program).filter_by(**kwargs)


def get_programs(session, **kwargs):
    return _get_programs(session, **kwargs).all()


def get_program_by_id(session, id):
    return session.query(models.Program).get(id)


def get_program_by_name(session, name):
    return _get_programs(session, name=name).one_or_none()


def _get_program_types(session, **kwargs):
    return session.query(models.ProgramType).filter_by(**kwargs)


def get_program_types(session, **kwargs):
    return _get_programs(session, **kwargs).all()


def get_program_type_by_id(session, id):
    return session.query(models.ProgramType).get(id)


def _get_program_settings(session, **kwargs):
    return session.query(models.ProgramSettings).filter_by(**kwargs)


def get_program_settings(session):
    return _get_program_settings(session).all()


def get_program_settings_by_program(session, program_id, **kwargs):
    return _get_program_settings(session, id=program_id, **kwargs).all()


def get_active_program_settings_by_program(session, program_id, **kwargs):
    return get_program_settings_by_program(session, program_id, active=1, **kwargs)
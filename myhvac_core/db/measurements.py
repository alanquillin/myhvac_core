from myhvac_core.db import models

from datetime import datetime


def get_sensor_measurements(session, **kwargs):
    return session.query(models.Measurement).filter_by(**kwargs).all()


def insert_sensor_measurement(session, sensor_id, type, data, **kwargs):
    if type == 'temperature':
        return insert_sensor_temperature(session, sensor_id, data.get('f'), **kwargs)


def get_sensor_temperatures(session, order_by=None, limit=None, order_desc=False, **kwargs):
    measurement_type = get_measurement_type(session, name='temperature')
    query = session.query(models.Measurement).filter_by(type_id=measurement_type.id, **kwargs)

    if order_by:
        if order_desc:
            query.order_by(order_by.desc())
        else:
            query.order_by(order_by)

    if limit:
        query.limit(limit)

    return query.all()


def insert_sensor_temperature(session, sensor_id, temp, **kwargs):
    measurement_type = get_measurement_type(session, name='temperature')
    measurement = models.Measurement(sensor_id=sensor_id, type_id=measurement_type.id,
                                     measurement=temp, recorded_date=datetime.now())

    session.add(measurement)
    return measurement


def _get_measurement_types(session, **kwargs):
    return session.query(models.MeasurementType).filter_by(**kwargs)


def get_measurement_types(session, **kwargs):
    return _get_measurement_types(session, **kwargs)


def get_measurement_type(session, **kwargs):
    return _get_measurement_types(session, **kwargs).one_or_none()

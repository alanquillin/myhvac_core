import logging

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, DateTime, Boolean, Table
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

LOG = logging.getLogger(__name__)


Base = declarative_base()


class SensorType(Base):
    __tablename__ = 'myhvac_sensor_types'
    id = Column(Integer, primary_key=True)
    model = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)


class Sensor(Base):
    __tablename__ = 'myhvac_sensors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    manufacturer_id = Column(String(255), nullable=True)
    sensor_type_id = Column(Integer, ForeignKey('myhvac_sensor_types.id'), nullable=True)
    sensor_type = relationship(SensorType)
    room_id = Column(Integer, ForeignKey('myhvac_rooms.id'), nullable=True)


class MeasurementType(Base):
    __tablename__ = 'myhvac_measurement_types'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(15), nullable=False)


class Measurement(Base):
    __tablename__ = 'myhvac_measurements'
    id = Column(BigInteger, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('myhvac_sensors.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('myhvac_measurement_types.id'), nullable=False)
    measurement = Column(Integer, nullable=False)
    recorded_date = Column(DateTime, nullable=False)
    measurement_type = relationship(MeasurementType)


class Room(Base):
    __tablename__ = 'myhvac_rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    active = Column(BIT, nullable=False)
    sensors = relationship(Sensor)

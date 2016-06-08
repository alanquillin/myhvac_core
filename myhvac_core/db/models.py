import logging

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, DateTime, Boolean, Table, Float, Time
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

LOG = logging.getLogger(__name__)


Base = declarative_base()


class ParseableModel(object):
    def to_dict(self):
        return self.__dict__

    def to_dict2(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))

        return d


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
    measurement = Column(Float, nullable=False)
    recorded_date = Column(DateTime, nullable=False)
    measurement_type = relationship(MeasurementType)


class Room(Base):
    __tablename__ = 'myhvac_rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    active = Column(BIT, nullable=False)
    weight = Column(Float, nullable=False)
    sensors = relationship(Sensor)


class ProgramType(Base):
    __tablename__ = 'myhvac_program_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    allow_override = Column(BIT, default=1)


class Program(Base, ParseableModel):
    __tablename__ = 'myhvac_programs'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    program_type_id = Column(Integer, ForeignKey('myhvac_program_types.id'), nullable=False)
    program_type = relationship(ProgramType)


class SystemConfig(Base):
    __tablename__ = 'myhvac_system_config'
    id = Column(Integer, primary_key=True)
    current_program_id = Column(Integer, ForeignKey('myhvac_programs.id'), nullable=False)
    current_program = relationship(Program)
    timestamp = Column(DateTime, nullable=False)
    active = Column(BIT, nullable=False)


class ProgramSettings(Base):
    __tablename__ = 'myhvac_program_settings'
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('myhvac_programs.id'), nullable=False)
    program = relationship(Program)
    day_of_week = Column(Integer, nullable=False)
    time_of_day = Column(Time, nullable=False)
    cool_threshold = Column(Integer, nullable=False)
    heat_threshold = Column(Integer, nullable=False)
    fan_on = Column(BIT, nullable=False, default=False)
    timestamp = Column(DateTime, nullable=False)
    active = Column(BIT, nullable=False)

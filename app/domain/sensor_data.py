from sqlalchemy import Column, BigInteger, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    temperature = Column(Integer, nullable=True)
    humidity = Column(Integer, nullable=True)
    electrical_conductivity = Column(Integer, nullable=True)
    co2 = Column(Integer, nullable=True)
    camera_data = Column(String, nullable=True)
    client_id = Column(BigInteger, nullable=False)
    uuid = Column(String, nullable=False)
    event = Column(String, nullable=False)
    datetime = Column(String, nullable=False)

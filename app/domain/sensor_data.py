from sqlalchemy import Column, String, Float, DateTime, BigInteger, INT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(BigInteger, primary_key=True)
    uuid = Column(String)
    temperature = Column(INT)
    humidity = Column(INT)
    electrical_conductivity = Column(INT)
    co2 = Column(INT)
    camera_data = Column(String)
    datetime = Column(DateTime)
    client_id = Column(INT)
    event = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'electrical_conductivity': self.electrical_conductivity,
            'co2': self.co2,
            'camera_data': self.camera_data,
            'date_time': self.datetime.isoformat() if self.datetime else None,
            'client_id': self.client_id,
            'event': self.event
        }

from sqlalchemy import Column, String, Float, DateTime, INT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensorData(Base):
    __tablename__ = 'sensor_data'

    uuid = Column(String, primary_key=True)
    temperature = Column(INT)
    humidity = Column(INT)
    electrical_conductivity = Column(INT)
    co2 = Column(INT)
    camera_data = Column(String)
    datetime = Column(DateTime)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'electrical_conductivity': self.electrical_conductivity,
            'co2': self.co2,
            'camera_data': self.camera_data,
            'date_time': self.datetime.isoformat() if self.datetime else None
        }

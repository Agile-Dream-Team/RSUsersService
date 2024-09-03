from sqlalchemy import Column, String, Boolean, TIMESTAMP, BigInteger, INT, Sequence, FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(BigInteger, Sequence('sensor_data_id_seq'), primary_key=True)
    temperature_global = Column(FLOAT)
    temperature_local = Column(FLOAT)
    humidity_global = Column(FLOAT)
    humidity_local = Column(FLOAT)
    movement = Column(Boolean)
    air_flow = Column(FLOAT)
    weight = Column(FLOAT)
    light_intensity = Column(FLOAT)
    uuid = Column(String, nullable=False)
    datetime = Column(TIMESTAMP)
    client_id = Column(FLOAT, nullable=False)
    event = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'temperature_global': self.temperature_global,
            'temperature_local': self.temperature_local,
            'humidity_global': self.humidity_global,
            'humidity_local': self.humidity_local,
            'movement': self.movement,
            'air_flow': self.air_flow,
            'weight': self.weight,
            'uuid': self.uuid,
            'datetime': self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'client_id': self.client_id,
            'event': self.event
        }

from sqlalchemy import Column, BigInteger, Sequence, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
from .base import Base


class Camera(Base):
    __tablename__ = 'camera'

    id = Column(BigInteger, Sequence('camera_id_seq'), primary_key=True)
    image_b64 = Column(VARCHAR)
    sensor_data_id = Column(BigInteger, ForeignKey('sensor_data.id'), nullable=False)

    sensor_data = relationship("SensorData", back_populates="cameras")

    def to_dict(self):
        return {
            'id': self.id,
            'image_b64': self.image_b64,
            'sensor_data_id': self.sensor_data_id
        }

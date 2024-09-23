from sqlalchemy.orm import Session
from app.domain.sensor_data import SensorData


class SensorDataRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, sensor_data: SensorData):
        try:
            self.db_session.add(sensor_data)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_all(self):
        return self.db_session.query(SensorData).all()

    def get_by_id(self, sensor_data_id):
        return self.db_session.query(SensorData).filter(SensorData.id == sensor_data_id).first()

    def delete(self, sensor_data):
        pass

    def update(self, sensor_data):
        pass





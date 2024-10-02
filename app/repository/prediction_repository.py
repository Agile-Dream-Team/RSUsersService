# app/repository/prediction_repository.py
from app.domain.prediction import Prediction
from app.domain.camera import Camera
from app.domain.sensor_data import SensorData


class PredictionRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_constructed_data(self, record_id):
        camera = self.db_session.query(Camera).filter_by(id=record_id).first()
        sensor_data = self.db_session.query(SensorData).filter_by(id=camera.sensor_data_id).first() if camera else None
        if camera and sensor_data:
            return Prediction(camera, sensor_data)
        return None

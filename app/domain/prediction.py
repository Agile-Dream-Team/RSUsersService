class Prediction:
    def __init__(self, camera, sensor_data):
        self.camera = camera
        self.sensor_data = sensor_data

    def to_dict(self):
        prediction_dict = {}
        if self.camera:
            prediction_dict.update(self.camera.to_dict())
        if self.sensor_data:
            prediction_dict.update(self.sensor_data.to_dict())
        return prediction_dict

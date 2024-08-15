from app.dto.kafka_in_dto import KafkaInDTO
from app.domain.sensor_data import SensorData

def map_dto_to_entity(kafka_in_dto: KafkaInDTO) -> SensorData:
    def safe_int_conversion(value: str) -> int:
        try:
            return int(float(value))
        except ValueError:
            print(ValueError) # or handle the error as needed

    return SensorData(
        temperature=safe_int_conversion(kafka_in_dto.data.temperature),
        humidity=safe_int_conversion(kafka_in_dto.data.humidity),
        electrical_conductivity=safe_int_conversion(kafka_in_dto.data.electrical_conductivity),
        co2=safe_int_conversion(kafka_in_dto.data.co2),
        camera_data=kafka_in_dto.data.camera_data,
        client_id=safe_int_conversion(kafka_in_dto.client_id),
        datetime=kafka_in_dto.date_time,
        uuid=kafka_in_dto.uuid,
        event=kafka_in_dto.event
    )

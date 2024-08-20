from enum import Enum


class EventType(str, Enum):
    NORMAL = "normal"
    HIGH_TEMP = "high_temp"
    LOW_TEMP = "low_temp"
    HIGH_HUMIDITY = "high_humidity"
    LOW_HUMIDITY = "low_humidity"
    HIGH_CO2 = "high_co2"
    LOW_CO2 = "low_co2"
    HIGH_ELECTRICITY = "high_electricity"
    LOW_ELECTRICITY = "low_electricity"
    CAM_ALERT = "cam_alert"
    UNKNOWN = "unknown"


class EventActionConsume(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    GET_ALL = "get_all"
    GET_BY_ID = "get_by_id"


class EventActionProduce(str, Enum):
    GET_ALL_PRODUCE = "get_all_produce"
    GET_BY_ID_PRODUCE = "get_by_id_produce"

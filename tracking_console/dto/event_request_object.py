from typing import List

from tracking_console.enum import DataTypeEnum


class FieldDTO:
    def __init__(self, field_name: str, data_types: List[DataTypeEnum]):
        self.__field_name = field_name
        self.__data_types = data_types

    @property
    def field_name(self) -> str:
        return self.__field_name

    @property
    def data_types(self) -> List[DataTypeEnum]:
        return self.__data_types

    @property
    def types(self) -> List[type]:
        return [obj.object for obj in self.__data_types]


class EventRequestObjectDTO:

    def __init__(self, required_fields: List[str], allowed_fields: List[FieldDTO]):
        self.__required_fields = required_fields
        self.__allowed_fields = allowed_fields

    @property
    def required_fields(self) -> List[str]:
        return self.__required_fields

    @property
    def allowed_fields(self) -> List[FieldDTO]:
        return self.__allowed_fields

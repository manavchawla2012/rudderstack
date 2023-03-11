from rudderstack.helpers.enum_helper import BaseEnum


class RuleTypeEnum(BaseEnum):
    OBJECT = ('object', 'object')


class DataTypeEnum(BaseEnum):
    string = ('string', ('string', str, lambda a: type(a) == str))
    number = ('number', ('number', int, lambda a: str(a).isnumeric()))

    @property
    def val(self):
        return self.data[0]

    @property
    def object(self) -> type:
        return self.data[1]

    def validate(self, inp) -> bool:
        return self.data[2](inp)

from datetime import datetime
from bot import DATE_TIME_FORMAT

from UI import UI_descriptors


class DateTime:
    """Try convert input value to DateTime, if can't then None

        Using: 
            1.Set own class argument with calling class object

            2.Set self argument with value

        Example:
            class A:
                x = DateTimeOrNone(format)

                def __init__(self, x):
                    self.x = x          
        Args:
            can_be_none: default False
        """

    def __init__(self, can_be_none: bool = False):
        self.__format = DATE_TIME_FORMAT
        self.__can_be_none = can_be_none

    def __set_name__(self, owner, name: str):
        self.__name = '_' + name

    def __get__(self, instance, owner) -> datetime:
        return getattr(instance, self.__name)

    def __set__(self, instance, value: any):
        if (self.__can_be_none and value is None) or (type(value) is datetime):
            pass
        else:
            try:
                value = datetime.strptime(str(value), self.__format)
            except TypeError:
                raise TypeError(UI_descriptors.get_date_time_type_error())
        if type(value) is datetime:
            value = value.replace(microsecond=0)
        setattr(instance, self.__name, value)
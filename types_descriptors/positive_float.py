from UI import UI_descriptors


class PositiveFloat:
    """Raise value exception when value < 0

        Using: 
            1.Set own class argument with calling class object

            2.Set self argument with value

        Example:
            class A:
                x = PositiveFloatOrNone()

                def __init__(self, x):
                    self.x = x
        Args:
            can_be_none: default False

            min_value: not required

            max_value: not required
        """

    def __init__(self, can_be_none: bool = False, min_value: int = None, max_value: int = None):
        self.__min = min_value
        self.__max = max_value
        self.__can_be_none = can_be_none

    def __set_name__(self, owner, name: str):
        self.__name = '_' + name

    def __get__(self, instance, owner) -> float:
        return getattr(instance, self.__name)

    def __set__(self, instance, value: float):
        if self.__can_be_none and value is None:
            pass
        else:
            try:
                value = float(value)
            except (TypeError, ValueError):
                raise TypeError(UI_descriptors.get_positive_float_type_error())
            except OverflowError:
                raise OverflowError(UI_descriptors.get_positive_float_overflow_error())
            if value < 0:
                raise ValueError(UI_descriptors.get_positive_float_less_than_0_error())
            if type(self.__min) is float and value < self.__min:
                raise ValueError(UI_descriptors.get_positive_float_min_error())
            if type(self.__max) is float and value > self.__max:
                raise ValueError(UI_descriptors.get_positive_float_max_error())

        setattr(instance, self.__name, value)
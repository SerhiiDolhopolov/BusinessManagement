from UI.language_resources import LanguageResources


__descriptors = LanguageResources().descriptors


def get_date_time_type_error() -> str:
    return __descriptors.get('date_time_type_error')

def get_positive_float_type_error() -> str:
    return __descriptors.get('positive_float_type_error')

def get_positive_float_overflow_error() -> str:
    return __descriptors.get('positive_float_overflow_error')

def get_positive_float_less_than_0_error() -> str:
    return __descriptors.get('positive_float_less_than_0_error')

def get_positive_float_min_error() -> str:
    return __descriptors.get('positive_float_min_error')

def get_positive_float_max_error() -> str:
    return __descriptors.get('positive_float_max_error')

def get_positive_int_type_error() -> str:
    return __descriptors.get('positive_int_type_error')

def get_positive_int_less_than_0_error() -> str:
    return __descriptors.get('positive_int_less_than_0_error')

def get_positive_int_min_error() -> str:
    return __descriptors.get('positive_int_min_error')

def get_positive_int_max_error() -> str:
    return __descriptors.get('positive_int_max_error')
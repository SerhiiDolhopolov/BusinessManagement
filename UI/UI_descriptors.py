from UI_base import get_text
from UI.language_resources import LanguageResources


__descriptors = LanguageResources().descriptors


def get_date_time_type_error():
    return get_text(__descriptors, 'date_time_type_error')
def get_positive_float_type_error():
    return get_text(__descriptors, 'positive_float_type_error')
def get_positive_float_overflow_error():
    return get_text(__descriptors, 'positive_float_overflow_error')
def get_positive_float_less_than_0_error(value):
    return get_text(__descriptors, 'positive_float_less_than_0_error', value=value)
def get_positive_float_min_error(value, min_value):
    return get_text(__descriptors, 'positive_float_min_error', value=value, min_value=min_value)
def get_positive_float_max_error(value, max_value):
    return get_text(__descriptors, 'positive_float_max_error', value=value, max_value=max_value)
def get_positive_int_type_error():
    return get_text(__descriptors, 'positive_int_type_error')
def get_positive_int_less_than_0_error(value):
    return get_text(__descriptors, 'positive_int_less_than_0_error', value=value)
def get_positive_int_min_error(value, min_value):
    return get_text(__descriptors, 'positive_int_min_error', value=value, min_value=min_value)
def get_positive_int_max_error(value, max_value):
    return get_text(__descriptors, 'positive_int_max_error', value=value, max_value=max_value)
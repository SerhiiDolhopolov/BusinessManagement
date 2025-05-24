from UI.language_resources import LanguageResources
import html 

__descriptors = LanguageResources().descriptors

def get_date_time_type_error() -> str:
    return html.escape(__descriptors.get('date_time_type_error'))

def get_positive_float_type_error() -> str:
    return html.escape(__descriptors.get('positive_float_type_error'))

def get_positive_float_overflow_error() -> str:
    return html.escape(__descriptors.get('positive_float_overflow_error'))

def get_positive_float_less_than_0_error(value) -> str:
    return html.escape(__descriptors.get('positive_float_less_than_0_error').format(value=value))

def get_positive_float_min_error(value, min_value) -> str:
    return html.escape(__descriptors.get('positive_float_min_error').format(value=value, 
                                                                            min_value=min_value))

def get_positive_float_max_error(value, max_value) -> str:
    return html.escape(__descriptors.get('positive_float_max_error').format(value=value,
                                                                            max_value=max_value))

def get_positive_int_type_error() -> str:
    return html.escape(__descriptors.get('positive_int_type_error'))

def get_positive_int_less_than_0_error(value) -> str:
    return html.escape(__descriptors.get('positive_int_less_than_0_error').format(value=value))

def get_positive_int_min_error(value, min_value) -> str:
    return html.escape(__descriptors.get('positive_int_min_error').format(value=value,
                                                                          min_value=min_value))

def get_positive_int_max_error(value, max_value) -> str:
    return html.escape(__descriptors.get('positive_int_max_error').format(value=value, max_value=max_value))
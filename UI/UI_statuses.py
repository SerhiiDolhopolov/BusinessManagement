from UI.language_resources import LanguageResources
from UI.base import get_text


__statuses = LanguageResources().statuses


def get_on_the_way() -> str:
    return get_text(__statuses, 'on_the_way')


def get_waiting_for_spares() -> str:
    return get_text(__statuses, 'waiting_for_spares')


def get_waiting_for_repairs() -> str:
    return get_text(__statuses, 'waiting_for_repairs')


def get_waiting_for_photo() -> str:
    return get_text(__statuses, 'waiting_for_photo')


def get_waiting_for_publication() -> str:
    return get_text(__statuses, 'waiting_for_publication')


def get_available() -> str:
    return get_text(__statuses, 'available')


def get_finished() -> str:
    return get_text(__statuses, 'finished')


def get_cancelled() -> str:
    return get_text(__statuses, 'cancelled')

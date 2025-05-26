from UI.language_resources import LanguageResources
from UI.base import get_text


__emoji = LanguageResources().emoji
__status = __emoji['status']


def get_on_the_way() -> str:
    return get_text(__status, 'on_the_way')


def get_waiting_for_spares() -> str:
    return get_text(__status, 'waiting_for_spares')


def get_waiting_for_repairs() -> str:
    return get_text(__status, 'waiting_for_repairs')


def get_waiting_for_photo() -> str:
    return get_text(__status, 'waiting_for_photo')


def get_waiting_for_publication() -> str:
    return get_text(__status, 'waiting_for_publication')


def get_available() -> str:
    return get_text(__status, 'available')


def get_finished() -> str:
    return get_text(__status, 'finished')


def get_cancelled() -> str:
    return get_text(__status, 'cancelled')


def get() -> str:
    return get_text(__status, '_')
from UI.language_resources import LanguageResources


__emoji = LanguageResources().emoji
__status = __emoji['status']


def get_on_the_way() -> str:
    return __status.get('on_the_way')


def get_waiting_for_spares() -> str:
    return __status.get('waiting_for_spares')


def get_waiting_for_repairs() -> str:
    return __status.get('waiting_for_repairs')


def get_waiting_for_photo() -> str:
    return __status.get('waiting_for_photo')


def get_waiting_for_publication() -> str:
    return __status.get('waiting_for_publication')


def get_available() -> str:
    return __status.get('available')


def get_finished() -> str:
    return __status.get('finished')


def get_cancelled() -> str:
    return __status.get('cancelled')


def get() -> str:
    return __status.get('_')
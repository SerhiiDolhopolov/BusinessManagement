from UI.language_resources import LanguageResources


__statuses = LanguageResources().statuses


def get_on_the_way() -> str:
    return __statuses.get('on_the_way')

def get_waiting_for_spares() -> str:
    return __statuses.get('waiting_for_spares')

def get_waiting_for_repairs() -> str:
    return __statuses.get('waiting_for_repairs')

def get_waiting_for_photo() -> str:
    return __statuses.get('waiting_for_photo')

def get_waiting_for_publication() -> str:
    return __statuses.get('waiting_for_publication')

def get_available() -> str:
    return __statuses.get('available')

def get_finished() -> str:
    return __statuses.get('finished')

def get_cancelled() -> str:
    return __statuses.get('cancelled')

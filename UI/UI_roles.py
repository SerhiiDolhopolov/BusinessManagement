from UI.language_resources import LanguageResources


__roles = LanguageResources().roles


def get_user() -> str:
    return __roles.get('user')


def get_courier() -> str:
    return __roles.get('courier')


def get_manager() -> str:
    return __roles.get('manager')


def get_admin() -> str:
    return __roles.get('admin')
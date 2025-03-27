from UI.language_resources import LanguageResources

__menu = LanguageResources().menu


def get_welcome() -> str:
    return __menu.get('welcome')

def get_user_registration_select_role(username: str) -> str:
    return __menu.get('user_registration_select_role').format(username=username)

def get_chat_with_admin_button(username: str) -> str:
    return f'{__menu.get('chat_with_admin_button')} {username}'
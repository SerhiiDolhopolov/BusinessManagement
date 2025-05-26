from UI.language_resources import LanguageResources
from UI_base import get_text

__menu = LanguageResources().menu
__admin_page = __menu['admin_page']
__models = __admin_page['models']
__colors = __admin_page['colors']
__defects = __admin_page['defects']
__memory = __admin_page['memory']


def get_info() -> str:
    return get_text(__admin_page, 'info')


def get_models_info() -> str:
    return get_text(__models, 'info')


def get_models_button() -> str:
    return get_text(__models, 'button')


def get_models_color_button() -> str:
    return get_text(__models, 'color_button')


def get_models_memory_button() -> str:
    return get_text(__models, 'memory_button')


def get_models_delete_button() -> str:
    return get_text(__models, 'delete_button')


def get_ask_new_model() -> str:
    return get_text(__models, 'ask_new')


def get_model_info(model: str) -> str:
    return get_text(__models, 'model_info', model=model)


def get_ask_select_colors(model: str) -> str:
    return get_text(__models, 'ask_select_colors', model=model)


def get_ask_select_memories(model: str) -> str:
    return get_text(__models, 'ask_select_memories', model=model)


def get_colors_info() -> str:
    return get_text(__colors, 'info')


def get_colors_button() -> str:
    return get_text(__colors, 'button')


def get_ask_new_color() -> str:
    return get_text(__colors, 'ask_new')


def get_defects_info() -> str:
    return get_text(__defects, 'info')


def get_defects_button() -> str:
    return get_text(__defects, 'button')


def get_ask_new_defect() -> str:
    return get_text(__defects, 'ask_new')


def get_memory_info() -> str:
    return get_text(__memory, 'info')


def get_memory_button() -> str:
    return get_text(__memory, 'button')


def get_ask_new_memory() -> str:
    return get_text(__memory, 'ask_new')
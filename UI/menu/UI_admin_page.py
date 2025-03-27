from UI.language_resources import LanguageResources


__menu = LanguageResources().menu
__admin_page = __menu['admin_page']
__models = __admin_page['models']
__colors = __admin_page['colors']
__defects = __admin_page['defects']
__memory = __admin_page['memory']


def get_info() -> str:
    return __admin_page.get('info')


def get_models_info() -> str:
    return __models.get('info')

def get_models_button() -> str:
    return __models.get('button')

def get_models_color_button() -> str:
    return __models.get('color_button')

def get_models_memory_button() -> str:
    return __models.get('memory_button')

def get_models_delete_button() -> str:
    return __models.get('delete_button')

def get_ask_new_model() -> str:
    return __models.get('ask_new')

def get_model_info(model: str) -> str:
    return __models.get('model_info').format(model=model)

def get_ask_select_colors(model: str) -> str:
    return __models.get('ask_select_colors').format(model=model)

def get_ask_select_memories(model: str) -> str:
    return __models.get('ask_select_memories').format(model=model)


def get_colors_info() -> str:
    return __colors.get('info')

def get_colors_button() -> str:
    return __colors.get('button')

def get_ask_new_color() -> str:
    return __colors.get('ask_new')


def get_defects_info() -> str:
    return __defects.get('info')

def get_defects_button() -> str:
    return __defects.get('button')

def get_ask_new_defect() -> str:
    return __defects.get('ask_new')


def get_memory_info() -> str:
    return __memory.get('info')

def get_memory_button() -> str:
    return __memory.get('button')

def get_ask_new_memory() -> str:
    return __memory.get('ask_new')
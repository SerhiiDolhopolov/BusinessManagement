from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import handlers.keyboards as keyboards


def get_show_objects_keyboard(
    obj_name: str,
    page: int,
    objects_on_page: dict[int, any],
    all_count: int,
    obj_count_on_page: int
) -> InlineKeyboardMarkup:
    """Returns keyboard with possible select button

    Args:
        obj_name (str): what object: 'colors', 'defects', 'memories'
        page (int): page
        objects_on_page (dict[int,any]): {object_id: (object, in_model)}
        all_count (int): count of all object
        obj_count_on_page (int): count all objects on a page

    Returns:
        InlineKeyboardMarkup: keyboard
    """
    keyboard_builder = InlineKeyboardBuilder()
    for obj_id, obj in objects_on_page.items():
        keyboard_builder.row(
            InlineKeyboardButton(
                text=str(obj),
                callback_data=f'{obj_name}|select|id:{obj_id}'
            )
        )
    keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page, f'{obj_name}|show|page', obj_count_on_page, all_count
        )
    )
    keyboard_builder.row(
        InlineKeyboardButton(text='➕', callback_data=f"{obj_name}|add|")
    )
    keyboard_builder.row(keyboards.get_back_button('admin_menu|show|'))
    return keyboard_builder.as_markup()


def get_model_show_objects_keyboard(
    model_id: int,
    obj_name: str,
    page: int,
    objects_on_page_with_flag: dict[int, tuple[any, bool]],
    all_count: int,
    obj_count_on_page: int
) -> InlineKeyboardMarkup:
    """Returns keyboard with possible selected button for model page

    Args:
        model_id (int): model id
        obj_name (str): what object: 'colors', 'defects', 'memories'
        page (int): page
        objects_on_page_with_flag (dict[int, tuple[any,bool]]): {object_id: (object, in_model)}
        all_count (int): count of all object
        obj_count_on_page (int): count all objects on a page

    Returns:
        InlineKeyboardMarkup: keyboard
    """
    keyboard_builder = InlineKeyboardBuilder()
    for obj_id, (obj, flag) in objects_on_page_with_flag.items():
        keyboard_builder.row(
            InlineKeyboardButton(
                text=f'{"✅" if flag else "❌"}{obj}',
                callback_data=(
                    f'model_{obj_name}|select|m_id:{model_id}&id:{obj_id}&page:{page}'
                )
            )
        )
    keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page,
            f'model_{obj_name}|show|m_id:{model_id}&page',
            obj_count_on_page,
            all_count
        )
    )
    keyboard_builder.row(
        keyboards.get_back_button(f'models|select|id:{model_id}')
    )
    return keyboard_builder.as_markup()

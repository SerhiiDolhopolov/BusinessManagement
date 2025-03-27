import json
from pathlib import Path
from bot import SETTINGS_PATH


class LanguageResources:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.roles = {
            'user': 'User',
            'courier': 'Courier',
            'manager': 'Manager',
            'admin': 'Admin',
        }
        self.statuses = {
            'on_the_way': 'On the way',
            'waiting_for_spares': 'Waiting for spares',
            'waiting_for_repairs': 'Waiting for repairs',
            'waiting_for_photo': 'Waiting for photo',
            'waiting_for_publication': 'Waiting for publication',
            'available': 'Available',
            'finished': 'Finished',
            'cancelled': 'Cancelled',
        }
        self.emoji = {
                'status': {
                    'on_the_way': '🚗',
                    'waiting_for_spares': '⚙️',
                    'waiting_for_repairs': '🛠',
                    'waiting_for_photo': '📸',
                    'waiting_for_publication': '📝',
                    'available': '📋',
                    'finished': '✅',
                    'cancelled': '❌',
                    '_': '',
                },
                'navigation': {
                    'back': '↩️',
                    'preview_page': '⬅️',
                    'current_page': '[{page}]',
                    'next_page': '➡️'
                },
                'money': '💵',
        }
        self.menu = {
            'welcome': "Welcome! Thanks a lot for registration!",
            'user_registration_select_role': "User @{username} was registrated. Do you want to change his role?",
            'chat_with_admin_button': "Chat with admin",
            'main_page': {
                'command_order': "/order - Search for order by id",
                'command_role': "/role - Set role",
                'command_backup': "/backup - Create backup",
                'additional_info': 'Menu:',
                'buttons': {
                    'my_phones': '📱 My phones',
                    'add': '+',
                    'available': '{emoji} Available',
                    'phones': '📱 Phones',
                    'need_spares': '{emoji} Need spares',
                    'need_repairs': '{emoji} Need repairs',
                    'users': '👤 Users',
                    'couriers': '📦 Couriers',
                    'managers': 'Ⓜ️ Managers',
                    'admin_panel': '🅰️ Admin panel',
                    'statistics': '📊 Statistics',
                },
            },
            'phones_page': {
                'info': '{emoji} Phones with status "{status}":',
                'all_phones_info': '📱 All phones:',
                'my_phones_info': '📱 My phones:',
                'status_button': '{emoji} {status}',
                'all_phones_status_button': '📱 All phones',
                'select_status': 'Select a status to show all phones with this status:',
                'phone_button': "{status_emoji}{title} {money_emoji}{price_selling}",
                'defect_need_spares': {
                    'ask_category': "Select the defect category for phones that need spares:",
                    'info': '📱 Phones with defect "{defect}", which are waiting for spares:',
                },
                'defect_need_repairs': {
                    'ask_category': "Select the defect category for phones that need repairs:",
                    'info': '📱 Phones with defect "{defect}", which are waiting for repairs:',
                }
            },
            'phone_page': {
                'title': '{status_emoji} {title}',
                'battery_status': '🔋 Battery status: {battery_status:>19}',
                'price_purchase': '💰 Price purchase: {price_purchase:>25}',
                'charges': '💸 Charges: {charges:>38}',
                'price_selling': '💵 Price: {price_selling:>44}',
                'profit': '🤑 Profit: {profit:>43}',
                'defects': '⚙️ Defects: {defects}',
                'comment': '💬 Comment: {comment}',
                'date_time': '{date_time}',
                'order': '📋 Order №{order}',
                'confirm_message_to_other_admin': "From {emoji_user}@{username}:\nOrder №{order_id}\n{text}",
                'order_button': 'Order №{order_id}',

                'buttons': {
                    'change_price_purchase': '🔄 Purchase',
                    'change_charges': '🔄 Charges',
                    'change_price_selling': '🔄 Price',
                    'change_memory': '🔄 Memory',
                    'change_battery': '🔄 Battery',
                    'change_defects': '🔄 Defects',
                    'change_status': '➡️ Status',
                    'solve_defect': '⚙️ Solve defect',
                    'history': '📜 History'
                },

                'change_price_purchase': {
                    'ask': ("The current price purchase: {value}"
                            '\n'
                            "Indicate the price purchase:"),
                    'confirm': ("The price purchase was changed successfully!"
                                '\n'
                                "{value_from} -> {value_to}"),
                },

                'change_charges': {
                    'ask': ("The current charges: {value}"
                            '\n'
                            "Indicate the charges:"),
                    'confirm': ("The charges was changed successfully!"
                                '\n'
                                "{value_from} -> {value_to}"),
                },

                'change_price_selling': {
                    'ask': ("The current price: {value}"
                            '\n'
                            "Indicate the price:"),
                    'confirm': ("The price was changed successfully!"
                                '\n'
                                "{value_from} -> {value_to}"),
                },

                'change_memory': {
                    'ask': ("The current memory size: {value}"
                            '\n'
                            "Choose the memory size:"),
                    'confirm': ("The memory size was changed successfully!"
                                '\n'
                                "{value_from} -> {value_to}"),
                },

                'change_battery_status': {
                    'ask': ("The current battery status: {value}"
                            '\n'
                            "Indicate the battery status, from 0 to 100:"),
                    'confirm': ("The battery status was changed successfully!"
                                '\n'
                                "{value_from} -> {value_to}"),
                },

                'change_defects': {
                    'ask': "If you want to change the defects for phone {model}, select from the list below:",
                    'confirm': ("The defects were changed successfully!"
                                '\n'
                                'The previous defects: {defects_from}'
                                '\n\n'
                                'The current defects: {defects_to}'),
                    'continue_button': 'Continue',
                },

                'change_status': {
                    'ask': ("The current status: {emoji}{status}"
                            '\n'
                            "Select the new status:"),
                    'ask_sure': ("Do you want to change order's status?"
                                 '\n'
                                 "{emoji_from}{status_from} -> {emoji_to}{status_to}"
                                 '\n'
                                 "For confirmation click button \'Confirm\' or write the comment."),
                    'confirm_button': 'Confirm',
                    'confirm': ("📋The order's status №{order_id} was changed successfully!"
                                '\n\n'
                                "{title}"
                                '\n'
                                "{emoji_from}{status_from} -> {emoji_to}{status_to}"
                                '\n\n'
                                '💬Comment: {comment}'
                                '\n\n'
                                '{date_time}')
                },

                'solve_defect': {
                    'ask': "If you want to solve the defects for phone {model}, choose from the list below:",
                    'confirm': ("The defect {defect} was solved."
                                '\n'
                                "The current defects: {defects}"),
                },
            },
            'users_page': {
                'users': "All users:\n{users}",
                'couriers': "Couriers:\n{users}",
                'managers': "Managers:\n{users}",
            },
            'admin_page': {
                'info': 'Admin panel:',
                'models': {
                    'info': 'Models:',
                    'button': 'Models',
                    'color_button': 'Color',
                    'memory_button': 'Memory',
                    'delete_button': '🗑',
                    'ask_new': "Write the name of the new model:",
                    'model_info': '{model}:',
                    'ask_select_colors': "Select available colors for model {model}:",
                    'ask_select_memories': "Select available memories for model {model}:",
                },
                'colors': {
                    'info': 'Colors:',
                    'button': 'Colors',
                    'ask_new': "Write the name of the new color:",
                },
                'defects': {
                    'info': 'Defects:',
                    'button': 'Defects',
                    'ask_new': "Write the name of the new defect:",
                },
                'memory': {
                    'info': 'Memory:',
                    'button': 'Memory',
                    'ask_new': "Write the new memory size:",
                }
            },
            'add_page': {
                'select_model': "Select the model:",
                'select_color': "Select the phone color:",
                'select_memory': "Select the amount of memory:",
                'ask_battery_status': "Indicate the battery status, from 0 to 100:",
                'select_defect': "If you want to add defects to the {model}, please select from the list below:",
                'continue_button': 'Continue',
                'ask_price_purchase': "Indicate the price at which the phone was purchased:",
                'ask_comment': 'To complete, click the "Confirm" button or write a comment.',
                'confirm_button': 'Confirm',
                'confirm_message': ("📋The order №{order_id} was added!"
                            '\n\n'
                            "{title}"
                            '\n'
                            "🔋 Battery status: {battery_status}"
                            '\n'
                            '💰 Price purchase: {price_purchase}'
                            '\n\n'
                            '⚙️ Defects: {defects}'
                            '\n\n'
                            '💬 Comment: {comment}'
                            '\n\n'
                            '{date_time}'),
                'confirm_message_to_other_admin': "From {emoji_user}@{username}:\n{text}",
                'order_button': 'Order №{order_id}',
            }
        }
        self.commands = {
            'role': {
                'ask': "Write user id, which you want to change role:",
                'select': "Select a role for @{username}:",
                'exception': {
                    'user_not_exist': "The user doesn't exist.",
                    'not_correct_id': "The Id doesn't correct.\nWrite please numbers:\n\nTo exit call /start.",
                },
                'change_role_message_for_admin': "You changed a role for @{username}:\n{old_role} -> {role}",
                'change_role_message_for_other_admins': "@{admin_username} changed a role for @{username}:\n{old_role} -> {role}",
                'change_role_message_for_user': "Your role has been changed to {role}",
            },
            'order': {
                'ask': "Indicate order id, which you want to find",
                'exception': {
                    'order_not_exist': "The order doesn't exist.",
                    'not_correct_id': "The Id doesn't correct. \nWrite please numbers:\n\nTo exit call /start",
                }
            },
            'backup': {
                'info': ("Statistic for {date}"
                         '\n'
                         'Statuses:'
                         '\n'
                         '{statuses}'
                         '\n\n'
                         '🤑 Profit: {profit}'
                         '\n'
                         '💵 Earned: {earned}'
                         '\n'
                         '💰 Spent: {spent}'
                         '\n'
                         '💸 Spent on purchasing: {spent_on_purchasing}'
                         '\n'
                         '💸 Spent on charges: {spent_on_charges}')
            }
        }
        self.statistics = {
            'summary_statistic': 'Summary statistic',
            'profit': '🤑 Profit',
            'income': '💵 Income',
            'spent': '💸 Spent',
            'price_purchase': 'Price purchase',
            'charges': 'Charges',
            'total_models': 'Total models',
            'total_defects': 'Total defects',
            'without_defect': 'Without defect',
            'chart_profit_phones': "Chart of profit relative to phones sold",
            'chart_profit_models': "Profit/quantity graph relative to models sold",
            'chart_profit_solved_defects': "Profit/quantity graph relative to corrected defects of sold models",
            'chart_profit_users': 'Revenue/quantity graph vs. number of phones sold by users who downloaded them',
            'all_statistic': "All statistic",
            'statistic_by_months': "Statistic by months",
            'statistic_by_years': "Statistic by years",
            'statistic_from': "Statistic from",
            'statistic_to': 'to',
            'by_days': 'By days',
            'by_months': 'By months',
            'by_years': 'By years',
            'for_preview_week': 'For preview week',
            'for_preview_month': 'For preview month',
            'for_current_week': 'For current week',
            'for_current_month': 'For current month',
            'for_7_days': 'For 7 days',
            'for_30_days': 'For 30 days',
            'for_31_days': 'For 31 days',
            'apply_filter': 'Apply filter',
        }
        self.descriptors = {
            'date_time_type_error': "Please enter a value, which can be converted in date with format YYYY-MM-DD HH:MM:SS!",
            'positive_float_type_error': "Please enter a real number!",
            'positive_float_overflow_error': "Please enter smaller number!",
            'positive_float_less_than_0_error': "The value must be >= 0. \nThe current value: {value}",
            'positive_float_min_error': "The value must be >= {min_value}. \nThe current value: {value}",
            'positive_float_max_error': "The value must be <= {max_value}. \nThe current value: {value}",
            'positive_int_type_error': "Please enter an integer!",
            'positive_int_less_than_0_error': "The value must be >= 0. \nThe current value: {value}",
            'positive_int_min_error': "The value must be >= {min_value}. \nThe current value: {value}",
            'positive_int_max_error': "The value must be <= {max_value}. \nThe current value: {value}"
        }

        self.load()

    def load(self):
        attrs = ''
        path = SETTINGS_PATH / Path('language.json')
        if path.exists():
            with open(path, 'r', encoding="utf-8") as file:
                attrs = json.loads(file.read())
            [self.__setattr__(key, value) for key, value in attrs.items()]
        else:
            with open(path, 'w', encoding="utf-8") as file:
                file.write(json.dumps(self.__dict__, indent=4))

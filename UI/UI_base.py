import html


def get_text(language_menu: dict[str, str], key: str, **kwargs) -> str:
    text = language_menu.get(key)
    if kwargs:
        text = text.format(**kwargs)
    return html.escape(text)
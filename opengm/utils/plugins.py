import logging
from math import ceil

from pyrogram.types import InlineKeyboardButton

LOGGER = logging.getLogger(__name__)
LOADED = []
HELPABLE = {}
HELPABLE_LOWER = {}


def register_plugin(plugin_name: str, help_text: str = None):
    if plugin_name not in LOADED:
        LOADED.append(plugin_name)
    if plugin_name not in HELPABLE and help_text:
        HELPABLE[plugin_name] = help_text
        HELPABLE_LOWER[plugin_name.lower()] = plugin_name
    LOGGER.info(f"Plugin '{plugin_name}' has been registered.")


async def paginate_plugins(
    page_n: int, module_dict: dict, prefix, chat=None
) -> list:
    modules = []
    module_dict = dict(sorted(module_dict.items()))
    if not chat:
        for x in module_dict:
            LOGGER.debug(module_dict[x])
            modules.append(
                InlineKeyboardButton(x, callback_data=f"{prefix}_module({x})")
            )
    else:
        for x in module_dict:
            modules.append(
                InlineKeyboardButton(x, callback_data=f"{prefix}_module({x})")
            )

    pairs = list(zip(modules[::2], modules[1::2]))
    if len(modules) % 2 == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / 7)
    modulo_page = page_n % max_num_pages
    # can only have a certain amount of buttons side by side
    if len(pairs) > 7:
        pairs = pairs[modulo_page * 7 : 7 * (modulo_page + 1)] + [
            (
                InlineKeyboardButton(
                    "<",
                    callback_data=f"{prefix}_prev({modulo_page})",
                ),
                InlineKeyboardButton(
                    ">",
                    callback_data=f"{prefix}_next({modulo_page})",
                ),
            )
        ]

    return pairs

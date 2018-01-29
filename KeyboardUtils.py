import copy

from emoji import emojize as em

from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup


class MafiaMarkup(InlineKeyboardMarkup):
    def __init__(self, inline_keyboard, **kwargs):
        super().__init__(inline_keyboard, **kwargs)

    def _to_page(self, page_num):
        pass

    def __add__(self, other):
        if self.inline_keyboard is None:
            return other

        return MafiaMarkup(self.inline_keyboard + other.inline_keyboard)

    def is_empty(self):
        return self.inline_keyboard is None


class KeyboardFactory:
    @classmethod
    def empty(cls):
        return MafiaMarkup(None)

    @classmethod
    def button(cls, text, callback_data, arguments=""):
        return MafiaMarkup([[cls.button_(text, callback_data, arguments)]])

    @classmethod
    def button_(cls, text, callback_data, arguments=""):
        if arguments != "":
            if isinstance(arguments, tuple):
                arguments = ",".join(arguments)
            arguments = '.' + str(arguments)

        if not isinstance(callback_data, str):
            callback_data = callback_data.__name__

        return Button(text, callback_data=str(f"{callback_data}{arguments}"))

    @classmethod
    def double_button(cls, left_text, left_callback, right_text, right_callback, left_arguments="", right_arguments=""):
        return MafiaMarkup([[cls.button_(left_text, left_callback, left_arguments),
                             cls.button_(right_text, right_callback, right_arguments)]])

    @classmethod
    def start_user(cls, open_stat_callback, get_access_callback):
        return MafiaMarkup(
            [
                [cls.button_(f"{em(':open_file_folder:')} Открыть статистику", open_stat_callback)],
                [cls.button_(f"{em(':question:')} Запросить доступ", get_access_callback)]
            ]
        )

    @classmethod
    def main(cls, start_evening_callback, statistick_menu_callback, players_menu_callback):
        return cls.button(f"{em(':hourglass:')} Начать вечер", callback_data=start_evening_callback.__name__) + \
               cls.button(f"{em(':bar_chart:')} Меню рейтинга", callback_data=statistick_menu_callback.__name__) + \
               cls.button(f"{em(':paperclip:')} Меню игроков", callback_data=players_menu_callback.__name__)

    @classmethod
    def players_with_emoji(cls, players, second_line_emoji, callback_player, callback_emoji):
        kb = cls.empty()

        if isinstance(players, dict):
            players = players.values()

        for player in players:
            kb += cls.double_button(left_text=str(player),
                                    left_callback=callback_player.__name__,
                                    left_arguments=str(player.id),

                                    right_text=second_line_emoji
                                    if not isinstance(second_line_emoji, list) else next(second_line_emoji),

                                    right_callback=callback_emoji.__name__,
                                    right_arguments=str(player.id))
        return kb


class MultiPageKeyboardFactory:
    def __init__(self, markup, page_size, post_kb=None) -> None:
        super().__init__()
        self._page_size = page_size
        self._markup_lines = {}

        self.page = 0

        self.post_kb = post_kb

        page = -1
        for index, line in enumerate(markup.inline_keyboard):
            if index % page_size == 0:
                page += 1
                self._markup_lines[page] = []
            self._markup_lines[page].append([line])

    def control_buttons(self) -> MafiaMarkup:
        kb = [KeyboardFactory.button_(text=em(":rewind:"),
                                      callback_data="to_page_callback",
                                      arguments="0"),
              KeyboardFactory.button_(text=em(":arrow_left:") + " Назад",  # TODO. Is word needed?
                                      callback_data="to_page_callback",
                                      arguments=str(self.page - 1)),
              KeyboardFactory.button_(text="Вперед " + em(":arrow_right:"),  # TODO. Is word needed?
                                      callback_data="to_page_callback",
                                      arguments=str(self.page + 1)),
              KeyboardFactory.button_(text=em(":fast_forward:"),
                                      callback_data="to_page_callback",
                                      arguments=str(len(self._markup_lines) - 1))]

        return MafiaMarkup([kb])

    def to_markup(self, page) -> MafiaMarkup:
        if page < 0:
            page = 0
        elif page >= len(self._markup_lines):
            page = len(self._markup_lines) - 1

        self.page = page
        kb = KeyboardFactory.empty()

        for line in self._markup_lines[page]:
            kb += copy.deepcopy(line)

        kb = MafiaMarkup(kb)

        if len(self._markup_lines) > 1:
            kb += self.control_buttons()

        if self.post_kb is not None:
            kb += self.post_kb

        return kb

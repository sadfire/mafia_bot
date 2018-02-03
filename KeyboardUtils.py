import copy

from emoji import emojize as em

from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup


def emoji_number(num=None) -> object:
    emoji = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    if int(num) > len(emoji) -1 :
        return "🆙"

    return emoji if num is None else emoji[int(num)]


class MafiaMarkup(InlineKeyboardMarkup):
    def __init__(self, inline_keyboard, **kwargs):
        super().__init__(inline_keyboard, **kwargs)

    def _to_page(self, page_num):
        pass

    def __add__(self, other):

        if self.inline_keyboard is None:
            return other

        if other is None or other.inline_keyboard is None:
            return self

        return MafiaMarkup(self.inline_keyboard + other.inline_keyboard)

    def is_empty(self):
        return self.inline_keyboard is None


class KeyboardFactory:
    @classmethod
    def empty(cls):
        return MafiaMarkup(None)

    @classmethod
    def button(cls, text, callback_data, arguments="") -> MafiaMarkup:
        return MafiaMarkup([[cls.button_simple(text, callback_data, arguments)]])

    @classmethod
    def button_simple(cls, text, callback_data, arguments="") -> Button:
        if arguments != "":
            if isinstance(arguments, tuple):
                arguments = ",".join(arguments)
            arguments = '.' + str(arguments)

        if not isinstance(callback_data, str):
            callback_data = callback_data.__name__

        return Button(text, callback_data=str(f"{callback_data}{arguments}"))

    @classmethod
    def double_button(cls, left_text, left_callback, right_text, right_callback, left_arguments="", right_arguments=""):
        return MafiaMarkup([[cls.button_simple(left_text, left_callback, left_arguments),
                             cls.button_simple(right_text, right_callback, right_arguments)]])

    @classmethod
    def start_user(cls, open_stat_callback, get_access_callback):
        return MafiaMarkup(
            [
                [cls.button_simple(f"{em(':open_file_folder:')} Открыть статистику", open_stat_callback)],
                [cls.button_simple(f"{em(':question:')} Запросить доступ", get_access_callback)]
            ]
        )

    @classmethod
    def main(cls, start_evening_callback, statistick_menu_callback, players_menu_callback,
             evening_message="Начать вечер", test_game_callback=None):
        return cls.button(f"{em(':hourglass:')} {evening_message}", callback_data=start_evening_callback.__name__) + \
               cls.button(f"{em(':bar_chart:')} Меню рейтинга", callback_data=statistick_menu_callback.__name__) + \
               cls.button(f"{em(':paperclip:')} Меню игроков", callback_data=players_menu_callback.__name__) + \
               (cls.button(f"{em(':paperclip:')} Начало Тестовой игры", callback_data=test_game_callback.__name__) \
            if test_game_callback is not None else None)


    @classmethod
    def action_line(cls, *buttons):
        kb = []
        for button in buttons:
            button = list(button)
            if len(button[0]) > 0 and ":" in button[0]:
                end_emoji_index = button[0].index(':', 1)
                button[0] = em(button[0][:end_emoji_index + 1]) + button[0][end_emoji_index + 1:]

            kb.append(cls.button_simple(button[0], button[1], button[2] if len(button) > 2 else buttons[0][2]))
        return MafiaMarkup([kb])

    @classmethod
    def players_with_action(cls, players, second_line_emoji, callback_player, callback_emoji):
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

    @classmethod
    def confirmation(cls, yes_callback, no_callback, yes_message=None, no_message=None, yes_argument=""):
        if yes_message is None:
            yes_message = "✅ Да"

        if no_message is None:
            no_message = "❌ Нет"

        return MafiaMarkup(
            [[cls.button_simple(yes_message, yes_callback, yes_argument), cls.button_simple(no_message, no_callback)]])

    @classmethod
    def close_button(cls):
        return cls.button(f"{em(':x:')} Закрыть", "delete_message_callback")

    @classmethod
    def empty_line(cls):
        return cls.button(em(":small_blue_diamond:"), callback_data="empty")


class MultiPageKeyboardFactory:
    def __init__(self, markup, page_size, post_kb=None) -> None:
        super().__init__()
        self._page_size = page_size
        self._markup_lines = {}

        self.page = 0

        self.post_kb = post_kb

        page = -1

        if markup.inline_keyboard is None:
            return

        for index, line in enumerate(markup.inline_keyboard):
            if index % page_size == 0:
                page += 1
                self._markup_lines[page] = []
            self._markup_lines[page].append([line])

    def control_buttons(self) -> MafiaMarkup:
        kb = [KeyboardFactory.button_simple(text=em(":rewind:"),
                                            callback_data="to_page_callback",
                                            arguments="0"),
              KeyboardFactory.button_simple(text=em(":arrow_left:"),
                                            callback_data="to_page_callback",
                                            arguments=str(self.page - 1)),
              KeyboardFactory.button_simple("{}/{}".format(self.page + 1, self.get_size()),
                                            "empty"),
              KeyboardFactory.button_simple(text=em(":arrow_right:"),
                                            callback_data="to_page_callback",
                                            arguments=str(self.page + 1)),
              KeyboardFactory.button_simple(text=em(":fast_forward:"),
                                            callback_data="to_page_callback",
                                            arguments=str(len(self._markup_lines) - 1))]

        return MafiaMarkup([kb])

    def is_empty(self):
        return len(self._markup_lines) == 0

    def get_size(self):
        return len(self._markup_lines)

    def to_markup(self, page) -> MafiaMarkup:
        page = int(page)
        if self.is_empty():
            return self.post_kb if self.post_kb is not None else KeyboardFactory.empty()

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

from emoji import emojize as em

from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup


class MafiaMarkup(InlineKeyboardMarkup):
    def __add__(self, other):
        if self.inline_keyboard is None:
            return other

        return MafiaMarkup(self.inline_keyboard + other.inline_keyboard)

    def is_empty(self):
        return len(self.inline_keyboard) == 0


class KeyboardFactory:
    @classmethod
    def empty(cls):
        return MafiaMarkup(None)

    @classmethod
    def button(cls, text, callback_data, arguments=""):
        return MafiaMarkup([[cls.__button(text, callback_data, arguments)]])

    @classmethod
    def __button(cls, text, callback_data, arguments=""):
        if arguments != "":
            if isinstance(arguments, tuple):
                arguments = ",".join(arguments)
            arguments = '.' + str(arguments)

        if not isinstance(callback_data, str):
            callback_data = callback_data.__name__

        return Button(text, callback_data=str(f"{callback_data}{arguments}"))

    @classmethod
    def double_button(cls, left_text, left_callback, right_text, right_callback, left_arguments="", right_arguments=""):
        return MafiaMarkup([[cls.__button(left_text, left_callback, left_arguments),
                             cls.__button(right_text, right_callback, right_arguments)]])

    @classmethod
    def start_user(cls, open_stat_callback, get_access_callback):
        return MafiaMarkup(
            [
                [cls.button(f"{em(':open_file_folder:')} Открыть статистику", open_stat_callback)],
                [cls.button(f"{em(':question:')} Запросить доступ", get_access_callback)]
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

                                    right_text=second_line_emoji,
                                    right_callback=callback_emoji.__name__,
                                    right_arguments=str(player.id))
        return kb
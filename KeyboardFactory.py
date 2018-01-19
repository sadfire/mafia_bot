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
        for id, player in players:
            kb += cls.double_button(left_text=str(player),
                                    left_callback=callback_player.__name__,
                                    left_arguments=str(id),

                                    right_text=second_line_emoji,
                                    right_callback=callback_emoji.__name__,
                                    right_arguments=str(id))
        return kb

        # @classmethod
        # def statistic_reply(cls):
        #     kb = [[Button("{} Игры".format(em(":memo:")), callback_data="OpenGameStat")],
        #           [Button("{} Вечера".format(em(":last_quarter_moon:")), callback_data="OpenEveningStat")]]
        #     return MafiaMarkup(kb)
        #
        # @classmethod
        # def approve(cls, param):
        #     return MafiaMarkup([[Button(em(":ok:"), callback_data=param + "_approve")]])
        #
        # @classmethod
        # def choose(cls, callback_prefix, params):
        #     kb = [([[Button(param, callback_data="{}.{}".format(callback_prefix, param))]]) for param in params]
        #     return MafiaMarkup(kb)
        #
        # @classmethod
        # def confirm(cls):
        #     return MafiaMarkup([[Button("Да", callback_data="yes"), Button("Нет", callback_data="no")]])
        #
        # @classmethod
        # def button(cls, text, callback=""):
        #     return MafiaMarkup([[Button(text, callback_data=callback)]])
        #
        # @classmethod
        # def button_line(cls, buttons_list):
        #     kb = []
        #     for button in buttons_list:
        #         kb.append(Button(button[0], callback_data=button[1]))
        #     return MafiaMarkup([kb])
        #
        # @classmethod
        # def turple_list_to_kb(cls, objects, callbacks, postfix) -> MafiaMarkup:
        #     kb = []
        #
        #     for obj in objects:
        #         kb_line = []
        #         for index, attribut in enumerate(obj):
        #             kb_line.append(Button(attribut, callback_data="{}_{}".format(
        #                 callbacks[attribut] if attribut in callbacks else attribut, postfix[index])))
        #         kb.append(kb_line)
        #
        #     return MafiaMarkup(kb)
        #
        # @classmethod
        # def players(cls, members, postfix="", emoji=None):
        #     kb = []
        #     if emoji is None:
        #         emoji = em(":x:")
        #
        #     id_postfix = ""
        #     if isinstance(postfix, tuple) and len(postfix) > 1:
        #         id_postfix = postfix[0]
        #         postfix = postfix[1]
        #
        #     if isinstance(emoji, list) and len(emoji) < len(members):
        #         emoji = em(":x:")
        #
        #     if isinstance(members, dict):
        #         members = members.values()
        #
        #     for member in members:
        #         kb.append([Button(member.name, callback_data=str(member.id) + id_postfix),
        #                    Button((emoji if not isinstance(emoji, list) else em(emoji.pop())),
        #                           callback_data=str(member.id) + postfix)])
        #     return MafiaMarkup(kb)
        #
        # @classmethod
        # def game_menu(cls, players, postfix=""):
        #     kb = []
        #     actions = {}
        #     for player in players:
        #         tmp = []
        #         tmp.append(Button(player.number, callback_data="{}{}".format(postfix, player.id)))

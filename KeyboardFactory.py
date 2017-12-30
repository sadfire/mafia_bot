from emoji import emojize as em
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Markup


class KBFactory:
    @staticmethod
    def start_user():
        return Markup([
            [Button("{0} Открыть статистику".format(em(":open_file_folder:")), callback_data="UserOpenStatistic")],
            [Button("{0} Запросить доступ".format(em(":question:")), callback_data="GetPermissions")]]
        )

    @staticmethod
    def stat_start_menu():
        kb = [[Button("{} Статистика по вечерам".format(em("")), callback_data="")],
              [Button("{} Статистика по играм".format(em("")), callback_data="")],
              [Button("{} Поменять город".format(em("")), callback_data="")]]

        return Markup(kb)

    @staticmethod
    def main():
        return Markup(
            [
                [Button("{} Начать вечер".format(em(":hourglass_flowing_sand:")), callback_data='start_evening')],

                [Button("{} Меню рейтинга".format(em(":bar_chart:")), callback_data='statistic_menu')],
                [Button("{} Меню игроков".format(em(":paperclip:")), callback_data='players_menu')]
            ])

    @classmethod
    def statistic_reply(cls):
        kb = [[Button("{} Игры".format(em(":memo:")), callback_data="OpenGameStat")],
              [Button("{} Вечера".format(em(":last_quarter_moon:")), callback_data="OpenEveningStat")]]
        return Markup(kb)

    @classmethod
    def approve(cls, param):
        return Markup([[Button(em(":ok:"), callback_data=param + "_approve")]])

    @classmethod
    def choose(cls, callback_prefix, params):
        kb = [([[Button(param, callback_data="{}.{}".format(callback_prefix, param))]]) for param in params]
        return Markup(kb)

    @classmethod
    def confirm(cls):
        return Markup([[Button("Да", callback_data="yes"), Button("Нет", callback_data="no")]])

    @classmethod
    def button(cls, text, callback=""):
        return Markup([[Button(text, callback_data=callback)]])

    @classmethod
    def turple_list_to_kb(cls, turpl_list) -> Markup:
        kb = []

        for attributs in turpl_list:
            kb_line = []
            for attribut in attributs:
                kb_line.append(Button(attribut[0], callback_data=attribut[1]))
            kb.append(kb_line)

        return Markup(kb)

    @classmethod
    def players(cls, members, postfix="", emoji=None):
        kb = []
        if emoji is None:
            emoji = em(":x:")

        id_postfix = ""
        if isinstance(postfix, tuple) and len(postfix) > 1:
            id_postfix = postfix[0]
            postfix = postfix[1]

        if isinstance(emoji, list) and len(emoji) < len(members):
            emoji = em(":x:")

        if isinstance(members, dict):
            members = members.values()

        for member in members:
            kb.append([Button(member.name, callback_data=str(member.id) + id_postfix),
                       Button((emoji if not isinstance(emoji, list) else em(emoji.pop())),
                              callback_data=str(member.id) + postfix)])
        return Markup(kb)

    @classmethod
    def game_menu(cls, players, postfix=""):
        kb = []
        actions = {}
        for player in players:
            tmp = []
            tmp.append(Button(player.number, callback_data="{}{}".format(postfix, player.id)))

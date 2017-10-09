import emoji
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

emoji_numbers = {
    1: ":one:",
    2: ":two:",
    3: ":three:",
    4: ":four:",
    5: ":five:",
    6: ":six:",
    7: ":seven:",
    8: ":eight:",
    9: ":nine:",
    10: ":ten:"
}

class KeyboardFactory:

    @staticmethod
    def start_keyboard(host_id):
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Начать вечер", callback_data=str(host_id) + '.start_evening')],

                [InlineKeyboardButton("Рейтинг игрока", callback_data=str(host_id) + '.open_stat'),
                 InlineKeyboardButton("Добавить игрока в базу", callback_data=str(host_id) + '.add_new_member')]
            ])

    @staticmethod
    def add_members(members):
        kb = []
        for member in members:
            kb.append([InlineKeyboardButton(member.name, callback_data="empty"),
                       InlineKeyboardButton(":-1:", callback_data="remove_member(" + member.id)])

        kb.append(
            [InlineKeyboardButton(emoji.emojize(":new:", use_aliases=True), callback_data="add_member")])

        return InlineKeyboardMarkup(kb)

    @staticmethod
    def game_citizen_view(citizens, mode):
        kb = []
        for citizen in citizens:
            kb.append([InlineKeyboardButton(emoji_numbers[citizen.number], callback_data="empty"),
                       InlineKeyboardButton(emoji.emojize(":point_up:"), callback_data="vote_" + citizen.member.id),
                       ])  # ToDo Think about it

        return InlineKeyboardMarkup(kb)

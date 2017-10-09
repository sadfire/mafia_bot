import logging, MySQLdb

from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler

from Factory import KeyboardFactory

from DatabaseApi import MafiaDB
from StringResourse import Resourse

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#
# class MafiaApi:
#     def __init__(self):
#         self.database = None
#         self.open_evenings = {}
#
#     @staticmethod
#     def start(bot, update):
#         # if not MafiaApi.check_permisson(update.effective_user.id):
#         #     update.message.reply_text("У вас нет доступа к рейтингу")
#         #     return
#
#         # MafiaApi.start_session(mafia_api.database, update.effective_user.id)
#
#         update.message.reply_text(
#             res["Hello"],
#             reply_markup=(KeyboardFactory.start_menu()))
#
#     @staticmethod
#     def add_new_member(bot, update):
#         update.message.reply_text(res["AddNewMember"])
#
#
#     @staticmethod
#     def add_member(bot, update):
#         update.message.reply_text(
#             res["AddMember"],
#             reply_markup=(KeyboardFactory.add_members()))
#
#
#     def start_evening(self):
#         pass
#
#     def open_stat(self):
#         pass
#
#     def add_user(self):
#         pass
#
#     @staticmethod
#     def button(bot, update):
#         pass
#
# def button(bot, update):
#     query = update.callback_query
#     data = query.data
#     tmp = "bot, update)"
#
#     if data[-1] != '(':
#         tmp = "(" + tmp
#
#     exec(data + tmp)
#
#
# def help(bot, update):
#     update.message.reply_text("Use /start to test this bot.")
#
#
# def error(bot, update, error):
#     logging.warning('Update "%s" caused error "%s"' % (update, error))
#

sessions = {}


class Session:
    def __init__(self, host, db_handler):
        self.host = host
        self.db_handler = db_handler
        self.message_wait_handler = None

    def start_menu(self, updater):
        updater.message.reply_text(
            Resourse["Hello"],
            reply_markup=KeyboardFactory.start_keyboard(self.host.telegram_id))

    def add_new_member(self, updater):
        if self.message_wait_handler is None:
            updater.effective_message.edit_text("Введите имя нового игрока")
            self.message_wait_handler = self.add_new_member
        else:
            pass


def start(bot, updater):
    id = updater.effective_chat.id
    if id in sessions.keys():
        return sessions[id].start_menu(updater)

    db_handler = MafiaDB("root", "")  # ToDo Поменять на ограниченого в правах юзера

    member = db_handler.get_member(id)

    if member is None:
        return Resourse["NoAccess"]

    if member.is_host:
        sessions[id] = Session(member, db_handler)
        return sessions[id].welcome_host_menu(updater)

    updater.message.reply_text(member.get_rate())  # ToDo Сделать красивый вывод inlin-ами

def button(bot, updater):
    query = updater.callback_query
    data = query.data.split('.')

    if len(data) < 2:
        return

    id = int(data[0])
    tmp = "sessions[id]." + data[1] + "("
    if id in sessions.keys():
        for index in range(len(data) - 2):
            tmp += data[index + 2] + ','
    tmp += "updater)"
    exec(tmp)

def get_session(bot, update):
    pass

def main():
    my_test_telegram_ip = 193019697
    db = MafiaDB("root", "")
    sessions[my_test_telegram_ip] = Session(db.get_member(my_test_telegram_ip), db)

    updater = Updater("381246435:AAFSryXBizl0-7mD7DPir62spub02PCFSZU")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    # updater.dispatcher.add_handler(CommandHandler('add_member', MafiaApi.add_member))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(get_session))

    updater.dispatcher.add_handler(CommandHandler('help', help))
    # updater.dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()

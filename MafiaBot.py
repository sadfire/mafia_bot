from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from DatabaseApi import MafiaDB
from MafiaSession import Session
from StringResourse import Commands, Resourse


class Bot:
    def __init__(self, updater):
        self.updater = updater
        self.sessions = {}
        self.db = MafiaDB("root", "")  # ToDo сделать других пользователей

    def start_bot(self):
        self._add_base_handlers()

        self.updater.start_polling()
        self.updater.idle()

    def _add_base_handlers(self):
        self.updater.dispatcher.add_handler(CommandHandler(Commands.Start, self._start))
        self.updater.dispatcher.add_handler(CommandHandler(Commands.Start, self._help))

    def _start(self, bot, update):
        t_id = update.effective_chat.id
        if t_id in self.sessions.keys():
            return

        member = self.db.get_member(t_id)

        if member is None:
            return update.message.reply_text(Resourse["NoAccess"])
        elif member.is_host:
            self.sessions[t_id] = Session(member, self.db)
            return self.sessions[t_id].start_menu(bot, update)
        else:
            return update.message.reply_text(member.get_rate())  # ToDo Сделать красивый вывод inlin-ами

    def _help(self, bot, update):
        pass

    def _serialize(self):
        pass

    def _unserialize(self):
        pass

    def get_session_from_file(self, file):
        pass  # ToDo Сделать забор из файла сериализованный сесссий

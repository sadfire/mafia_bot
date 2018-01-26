from Game.Member import Member


class Bot:
    def __init__(self) -> None:
        super().__init__()
        self.index = 0
        self._logs = []

    def send_message(self, chat_id, text, reply_markup=None):
        self._logs.append("bot send message with text \n {}\n".format(text))
        return self

    def edit_reply_markup(self, reply_markup):
        self._logs.append("edit reply markup")
        return self

    @property
    def message_id(self):
        self.index += 1
        return self.index

    @property
    def chat_id(self):
        return 0

    def delete_message(self, chat_id, message_id):
        self._logs.append("delete message with chat {} and id")

    def edit_message_reply_markup(self, chat_id, message_id, reply_markup):
        self._logs.append("edit message reply markup message {} with chat {} and id".format(message_id, chat_id))


class Updater:
    def __init__(self) -> None:
        super().__init__()
        self.dispatcher = self
        self._handlers = []
        self._logs = []

    def add_handler(self, handler):
        self._handlers.append(handler)
        self._logs.append("add handler {}".format(handler.__class__.__name__))

    def remove_handeler(self, handler):
        if handler in self._handlers:
            self._handlers.remove(handler)
            self._logs.append("remove handler {}".format(handler.__class__.__name__))
        else:
            self._logs.append("can't remove handler {}".format(handler.__class__.__name__))


class Database:
    def __init__(self, id, passw) -> None:
        super().__init__()
        self.logs = []
        self.logs.append("Database connect for {}@{}".format(id, passw))

    def get_member_by_telegram(self, t_id) -> Member:
        return Member(0, "HOST", True, t_id=t_id)

    def find_member(self, text):
        return Member(int(text), "USER_{}".format(text), True, t_id=1)

    def get_member(self, id):
        return Member(id, "USER_{}".format(id), True, t_id=1)

    def get_regular_members_by_host(self, *args):
        return [self.get_member(i) for i in range(10)]

class Update:
    def __init__(self, data='') -> None:
        super().__init__()
        self.data = data
        self.chat_id = 0
        self._logs = []

    @property
    def text(self):
        return self.data

    @property
    def effective_chat(self):
        return self

    @property
    def id(self):
        return 0

    @property
    def from_user(self):
        return self

    @property
    def username(self):
        return "USER"

    @property
    def effective_message(self):
        return self

    def edit_reply_markup(self, reply_markup):
        pass

    @property
    def callback_query(self):
        return self

    def edit_text(self, text):
        self._logs.append("update: edit text for {}".format(text))

from Game.Member import Member


class Bot:

    def __init__(self) -> None:
        super().__init__()
        self.index = 0

    def send_message(self, chat_id, text, reply_markup=None):
        print("bot send message with text \n {}\n".format(text))
        return self

    def edit_reply_markup(self, reply_markup):
        print("edit reply markup")
        return self

    @property
    def message_id(self):
        self.index += 1
        return self.index

    def delete_message(self, chat_id, message_id):
        print("delete message with chat {} and id")

class Updater:
    def __init__(self) -> None:
        super().__init__()
        self.dispatcher = self
        self._handlers = []

    def add_handler(self, handler):
        self._handlers.append(handler)
        print("add handler {}".format(handler.__class__.__name__))

    def remove_handeler(self, handler):
        if handler in self._handlers:
            self._handlers.remove(handler)
            print("remove handler {}".format(handler.__class__.__name__))
        else:
            print("can't remove handler {}".format(handler.__class__.__name__))


class Database:
    def __init__(self, id, passw) -> None:
        super().__init__()
        print("Database connect for {}@{}".format(id, passw))

    def get_member_by_telegram(self, t_id) -> Member:
        return Member(0, "HOST", True, t_id=t_id)

    def find_member(self, text):
        return Member(int(text), "USER_{}".format(text), True, t_id=1)

class Update:
    def __init__(self, data='') -> None:
        super().__init__()
        self.data = data
        self.chat_id = 0

    @property
    def text(self):
        return self.data

    @property
    def effective_message(self):
        return self

    @property
    def callback_query(self):
        return self

    def edit_text(self, text):
        print("update: edit text for {}".format(text))

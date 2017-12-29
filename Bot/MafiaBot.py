from telegram.ext import Updater


class MafiaBot:
    def __init__(self, token, session_filename) -> None:
        super().__init__()
        self._updater = Updater(token)
        self._session_filename = session_filename

    def __del__(self):
        self.serialize_sessions()

    def start(self):
        pass

    def get_serialized_sessions(self, filename):
        pass

    def serialize_sessions(self):
        pass
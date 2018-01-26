from SessionHandler.States import IState, get_query_text


class GameInProcess(IState):
    def process_callback(self, bot, update):
        data = get_query_text(update)
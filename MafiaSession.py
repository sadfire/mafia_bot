from MafiaView import View


class Session:
    def __init__(self, host, updater) -> None:
        super().__init__()
        self.host = host
        self.view = View(self, host.t_id, updater)

    def start_menu(self, bot, upd):
        self.view.start_menu(bot, upd)

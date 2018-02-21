from threading import Timer as timer
from Utils import kbf


class Timer:
    def __init__(self, seconds, update_callback, step=5) -> None:
        super().__init__()
        if seconds < step:
            raise ValueError("Low seconds")

        self.step = step
        self.current = seconds
        self._update_callback = update_callback
        self._start_timer(False)

    def _start_timer(self, is_start: bool = True):
        self._timer = timer(self.step, self.update)
        if is_start:
            self._timer.start()

    def play(self):
        pass

    @property
    def is_active(self):
        return self._timer.is_alive()

    def update(self):
        self.current -= self.step
        if self.current == 0:
            return self.stop

    def pause(self):
        pass

    def stop(self):
        pass


class TimerMessageHandler:
    def __init__(self, session, current_player, callback, seconds=60):
        self._session = session
        self._current_player = current_player
        self._callback = callback
        self._timer = Timer(seconds, self.update)
        self._message = self._session.send_message(self.get_message_string, self.get_message_kb)

    def update(self):
        self._session.edit_message(self.get_message_string, self.get_message_kb)

    def callback(self, action): return getattr(self._timer, action)()

    @property
    def get_message_string(self):
        return "Минута игрока {}\nОсталось {} секунд.".format(self._current_player.get_num_str, self._timer.current)

    @property
    def get_message_kb(self):
        if self._timer.is_active:
            button = ("⏸", self._callback, self._timer.pause)
        else:
            button = ("▶", self._callback, self._timer.play)

        return kbf.action_line(button, ("⏹", self._callback, self._timer.stop))

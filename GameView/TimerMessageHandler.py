from threading import Thread, Lock
from time import sleep

from Utils import kbf


class Timer:
    def __init__(self, seconds, update_callback, step=5) -> None:
        super().__init__()
        if seconds < step:
            raise ValueError("Low seconds")

        self.step = step
        self.current = seconds

        self._update_callback = update_callback

        self.is_active = False

        self.timer_loop_thread = Thread(target=self._timer_loop)
        self.timer_loop_thread.start()

    def play(self):
        self.is_active = True
        self._update_callback()

    def pause(self):
        self.is_active = False
        self._update_callback()

    def stop(self):
        self.current = 0
        self.is_active = False
        self._update_callback()

    def _timer_loop(self):
        while self.current > 0:
            sleep(1)

            if not self.is_active:
                continue

            if self.current % self.step == 0:
                self._update_callback()
            self.current -= 1
        self.stop()


class TimerMessageHandler:
    def __init__(self, session, current_player, callback, stop_callback, seconds=60):
        if seconds is 0:
            seconds = 60

        self._session = session
        self._current_player = current_player
        self._callback = callback
        self._stop_callback = stop_callback
        self._timer = Timer(seconds, self.update)

        self.message = self._session.send_message(self.get_message_string, self.get_message_kb)

    @property
    def get_current_seconds(self):
        return self._timer.current

    def update(self):
        if self._timer.current == 0:
            self._session.edit_message(self.message, "Минута игрока {} закончилась.".format(self._current_player.get_num_str))
            self._stop_callback(self._current_player.number)
        else:
            self._session.edit_message(self.message, self.get_message_string, self.get_message_kb)

    def callback(self, action):
        return getattr(self._timer, action)()

    @property
    def get_message_string(self):
        return "Минута игрока {}\nОсталось {} секунд.".format(self._current_player.get_num_str, self._timer.current)

    @property
    def get_message_kb(self):
        if self._timer.is_active:
            button = ("⏸", self._callback, self._timer.pause.__name__)
        else:
            button = ("▶", self._callback, self._timer.play.__name__)

        return kbf.action_line(button, ("⏹", self._callback, self._timer.stop.__name__))

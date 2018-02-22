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

        self._lock = Lock()
        self._lock.acquire(blocking=False)
        self.is_active = False

        self.timer_loop_thread = Thread(target=self._timer_loop)
        self.timer_loop_thread.start()

    def play(self):
        self.is_active = True
        self._lock.release()

    def pause(self):
        self.is_active = False
        self._lock.acquire(blocking=False)

    def stop(self):
        self.is_active = False
        self.current = 0

    def _timer_loop(self):
        while self.current != 0:
            self._lock.acquire()
            sleep(1)
            if self.current % self.step == 0:
                self._update_callback()
            self.current -= 1
            self._lock.release()


class TimerMessageHandler:
    def __init__(self, session, current_player, callback, seconds=60):
        self._session = session
        self._current_player = current_player
        self._callback = callback
        self._timer = Timer(seconds, self.update)

        self._message = self._session.send_message(self.get_message_string, self.get_message_kb)

    def update(self):
        if self._timer == 0:
            self._session.edit_message(self._message, "Минута игрока {} закончилась.".format(self._current_player.get_num_str))
        else:
            self._session.edit_message(self._message, self.get_message_string, self.get_message_kb)

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

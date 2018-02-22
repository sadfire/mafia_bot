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

        self._mutex = Lock()
        self._mutex.acquire()

        self.timer_loop_thread = Thread(target=self._timer_loop)
        self.timer_loop_thread.start()

    @property
    def is_active(self):
        return self._mutex.acquire(blocking=False)

    def play(self):
        self._mutex.release()

    def pause(self):
        self._mutex.acquire()

    def stop(self):
        self.current = 0

    def _timer_loop(self):
        while self.current != 0:
            if self._mutex.acquire(blocking=False):
                continue

            sleep(1)
            self.current -= 1
            if self.current % self.step == 0:
                self._update_callback()


class TimerMessageHandler:
    def __init__(self, session, current_player, callback, seconds=60):
        self._session = session
        self._current_player = current_player
        self._callback = callback
        self._timer = Timer(seconds, self.update)

        self._message = self._session.send_message(self.get_message_string, self.get_message_kb)

    def update(self):
        self._session.edit_message(self.get_message_string, self.get_message_kb)

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

from enum import Enum
from threading import Timer as timer

import time


class States(Enum):
    Play = 0
    Pause = 1
    Stop = 2


class Timer:
    def __init__(self, seconds, callback_process, callback_stop=None, args=(),
                 timeouts_count=12):

        self.args = args
        self.callbacks = {
            States.Play: callback_process,
            States.Stop: callback_stop
        }

        self.is_active = False

        self.current = seconds
        self.update_timeout = self.current / timeouts_count
        self.timer = None

    def start(self):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = timer(self.update_timeout, self.process)
        self.timer.start()

    def pause(self):
        self.is_active = False
        self.timer.cancel()

    def stop(self):
        self.pause()
        self._callback(States.Stop)

    def process(self):
        if not self.is_active:
            return

        self.current -= self.update_timeout
        self._callback(States.Play)

        if self.current != 0:
            self.start()
        else:
            self.stop()

    def _callback(self, state: States):
        callback = self.callbacks[state]
        if callback is not None:
            callback(self.args)

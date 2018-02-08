import time

from GameView.Timer import Timer


def timer_test():
    timer = Timer(seconds=10,
                  callback_process=lambda h: print(h, "Process"),
                  callback_stop=lambda h: print(h, "Stop"),
                  args=("World", "Condor"))
    timer.start()
    while True:
        time.sleep(10)

if __name__ == "__main__":
    timer_test()
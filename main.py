import logging

from MafiaBot import Bot


def main():
    bot = Bot("381246435:AAF0F3U0E_KPbc8iDKCkhwuSyuKkH4bNqz4")
    bot.start()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()

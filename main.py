import logging

from MafiaBot import Bot


def main():
    bot = Bot("381246435:AAFSryXBizl0-7mD7DPir62spub02PCFSZU")
    bot.start()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()

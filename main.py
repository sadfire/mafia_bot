import logging

from MafiaBot import Bot


def main():
    bot = Bot("381246435:AAHOxVWGkOvk7cLsvfUl2l00Ulb6RiIxDus")
    bot.start()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()

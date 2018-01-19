import logging

from MafiaBot import Bot
import sys

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    bot = Bot(sys.argv[1])
    bot.start()


if __name__ == "__main__":
    main()

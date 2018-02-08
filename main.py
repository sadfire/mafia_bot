import logging
import sys

from _mysql_exceptions import OperationalError

from MafiaBot import Bot
from Utils.MafiaDatabaseApi import Database as db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    try:
        db_mafia = db('bot', 'YWqYvadPZ35eDHDs')
    except OperationalError:
        logging.error("Mafia database shut down")
        return

    bot = Bot(sys.argv[1], db_mafia)
    bot.start()

if __name__ == "__main__":
    main()

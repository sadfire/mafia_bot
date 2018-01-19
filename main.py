import logging

from MafiaBot import Bot


def main():
    Bot("461567544:AAE2NhXbWIYDQfw2C3va4cY1-USBf9JGOx8").start()



if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()

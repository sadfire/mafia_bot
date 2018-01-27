from SessionHandler.Session import Session
from Tests import Mocks
import unittest

from Tests.Mocks import Update
from UserHandler import UserHandler


class MafiaTest(unittest.TestCase):
    def test_main_scenario(self):
        bot = Mocks.Bot()
        updater = Mocks.Updater()

        bot._sessions[0] = Session(bot, updater, 0, Mocks.Database)
        bot.query_callback(bot, Mocks.Update("_evening_manager_callback"))

        for member_id in range(0, 10):
            bot.query_callback(bot, Mocks.Update("_add_member_callback.{}".format(str(member_id))))

        bot.query_callback(bot, Mocks.Update("_end_evenings_callback"))
        bot.query_callback(bot, Mocks.Update("_choose_player_callback.1"))
        bot.query_callback(bot, Mocks.Update("_choose_number_callback.1"))

if __name__ == "__main__":
    unittest.main()

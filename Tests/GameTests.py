from SessionHandler.Session import Session
from Tests import Mocks
import unittest

from Tests.Mocks import Update
from UserHandler import UserHandler


class MafiaTest(unittest.TestCase):
    def test_main_scenario(self):
        bot = Mocks.Bot()
        updater = Mocks.Updater()

        session = Session(bot, updater, 0, Mocks.Database)
        session.query_callback(bot, Mocks.Update("_evening_manager_callback"))

        for member_id in range(0, 10):
            session.query_callback(bot, Mocks.Update("_add_member_callback.{}".format(str(member_id))))

        session.query_callback(bot, Mocks.Update("_end_evenings_callback"))
        session.query_callback(bot, Mocks.Update("select_member_0"))
        session.query_callback(bot, Mocks.Update("select_number_1"))

if __name__ == "__main__":
    unittest.main()

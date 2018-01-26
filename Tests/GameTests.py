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

        session.query_callback(bot, Mocks.Update("end_evening_adding_approve"))
        session.query_callback(bot, Mocks.Update("select_member_0"))
        session.query_callback(bot, Mocks.Update("select_number_1"))

    def test_user_scenario(self):
        bot = Mocks.Bot()
        updater = Mocks.Updater()

        handler = UserHandler(Mocks.Database("", ""))
        handler.start_callback(bot, Update())
        handler.query_callback(bot, Update("_user_open_statistic_callback"))


if __name__ == "__main__":
    unittest.main()

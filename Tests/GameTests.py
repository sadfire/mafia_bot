from SessionHandler.Session import Session
from Tests import Mocks
import unittest


class MafiaTest(unittest.TestCase):
    def test_main_scenario(self):
        bot = Mocks.Bot()
        updater = Mocks.Updater()

        session = Session(bot, updater, 0, Mocks.Database)
        session.query_callback(bot, Mocks.Update(""))
        session.query_callback(bot, Mocks.Update("start_evening"))
        for member_id in range(0, 10):
            session.state._add_member(bot, Mocks.Update(str(member_id)))
        session.query_callback(bot, Mocks.Update("end_evening_adding_approve"))
        session.query_callback(bot, Mocks.Update("1_select_member"))
        session.query_callback(bot, Mocks.Update("0_select_number"))

if __name__ == "__main__":
    unittest.main()

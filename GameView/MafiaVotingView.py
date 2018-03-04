from GameLogic import Cards, Game, Event, GameInfo, Roles
from GameView import IGameView

from GameLogic.Models import VotingModel

from Utils.KeyboardUtils import MafiaMarkup, KeyboardFactory as kbf, emoji_number as emn


class MafiaVotingView(IGameView):
    def __init__(self, session, game: Game, model=None):
        super().__init__(session, game, VotingModel(game, True))

        self.req_initiator = None

    @property
    def _next(self):
        if self._next_state  is not None:
            return self._next_state
        else:
            from GameView.IntroductionView import IntroductionView
            return IntroductionView, False

    def _greeting(self):
        self._message = self._session.send_message(text="Приветствую тебя мафия.\n"
                                                        "Кого будем убивать этой ночью?",
                                                   reply_markup=self.vote_keyboard)

    @property
    def vote_keyboard(self) -> MafiaMarkup:
        kb = kbf.empty()
        for card in self._model.available_cards:
            kb += kbf.button(Cards.get_name(card), self.ask_mafia_card, card.value)

        kb += kbf.button("🔪 Никого", self.kill_callback, -1)

        for number in self._model.get_candidate:
            kb += kbf.button(f"🔪 Игрока {emn(number)}", self.kill_confirm_callback, number)

        return kb

    def update_callback(self, bot, update):
        self._session.edit_message(message=self._message,
                                   text="Приветствую тебя мафия. Кого будем убивать этой ночью?",
                                   reply_markup=self.vote_keyboard)

    def kill_confirm_callback(self, bot, update, number):
        self._session.edit_message(self._message,
                                   text="🔪 Убиваем игрока {}?".format(emn(number)),
                                   reply_markup=kbf.confirmation(no_callback=self.update_callback,
                                                                 yes_callback=self.kill_callback,
                                                                 yes_message="🔪 Да",
                                                                 yes_argument=number))

    def kill_callback(self, bot, update, number):
        number = int(number)
        if number is -1:
            self._session.edit_message(self._message, f"Никто не под прицелом.")
        else:
            self._model.init_target(number)
            self._session.edit_message(self._message, f"Игрок {emn(number)} на грани жизни и смерти.")

        self._model.final()
        self._session.to_next_state()

    def ask_mafia_card(self, bot, update, card_id):
        self._session.delete_message_callback(bot, update)

        card = Cards(card_id)
        if card is Cards.Recruitment:
            from GameView import CardView
            from GameLogic.Models.Cards import RecruitmentModel
            self._next_state = CardView, RecruitmentModel
            self._session.to_next_state()


    def recruitment_callback(self, bot, update, mafia_number):
        mafia_number = int(mafia_number)
        self.game[mafia_number][GameInfo.IsCardSpent] = True
        self.game.wasted_cards.append(Cards.Recruitment)
        self.req_initiator = mafia_number

        kb = kbf.empty()
        for number in self.game.get_civilian_number:
            kb += kbf.button(emn(number), self.recruitment_process_callback, number)
        self._session.edit_message(self._req_message, "Кого вербуем?", reply_markup=kb)

    def recruitment_process_callback(self, bot, update, number):
        number = int(number)
        self.game[number][GameInfo.Role] = Roles.Mafia
        self.game.log_event(Event.Recruitment, initiator_players=self.req_initiator, target_player=number)
        self._session.edit_message(self._req_message, "Завербован {}".format(emn(number)))

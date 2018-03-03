from enum import Enum


class Cards(Enum):
    Neutral = 1
    Alibi = 2
    Banzai = 3
    FlakJacket = 4
    Waru = 5
    Recruitment = 6
    Zen = 7
    YinYang = 8
    Keiko = 9
    Kitsune = 10
    Theft = 11
    Mole = 12
    Rat = 13
    Heal = 14
    Leader = 15
    Mina = 16
    Retirement = 17
    Demoman = 18
    Ghost = 19
    Listener = 20
    Sensei = 21
    ChangeRole = 22
    Shuriken = 23
    Fugue = 24
    Harakiri = 25
    Yakuza = 26
    Undercover = 28
    TheLastShot = 29
    Exposure = 30
    DeadlyShot = 31

    @staticmethod
    def get_name(card) -> str:
        from Utils import Database
        return "{0} {1} {0}".format("🎴", Database().get_card_name(card.value))

    @staticmethod
    def is_day_card(card) -> bool:
        if isinstance(card, int):
            card = Cards(card)
        return card in [Cards.Alibi, Cards.Theft, Cards.Retirement]

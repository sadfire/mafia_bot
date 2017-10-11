from enum import Enum

Resourse = {
    "Hello": "Приветствую! Это бот учета рейтинга игроков мафии по правилам 'Город Спит' \n",
    "AddNewMember": "Вы можете добавить игрока в рейтинг. Введите его имя, если жалеате продолжить"
}

class Callback(Enum):
    StartEvening = 0,
    OpenStat = 1,
    AddNewMember = 2,
    AddPlayer = 3.
    RemovePlayer = 4,
    ConfirmationYes = 5,
    ConfirmationNo = 5,

class Commands(Enum):
    Start = "start"
    Help = "help"

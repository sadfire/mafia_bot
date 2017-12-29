import MySQLdb

class MafiaDB:
    def __init__(self, user, passw):
        self.db = MySQLdb.connect(host="localhost", user=user, passwd=passw, db="mafia_rate", charset='utf8')
        # формируем курсор, с помощью которого можно исполнять SQL-запросы
        self.cursor = self.db.cursor()

    def get_member(self, telegram_id):
        self.cursor.execute("SELECT * FROM `Members` WHERE IdTelegram = 193019697;")
        result = self.cursor.fetchall()
        if len(result) == 0:
            return None
        tmp_member = result[0]
        return Member(tmp_member[0], tmp_member[1], telegram_id, tmp_member[2] == 1)
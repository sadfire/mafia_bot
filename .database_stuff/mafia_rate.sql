-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               5.6.37 - MySQL Community Server (GPL)
-- Операционная система:         Win32
-- HeidiSQL Версия:              9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Дамп структуры базы данных mafia_rate
CREATE DATABASE IF NOT EXISTS `mafia_rate` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `mafia_rate`;

-- Дамп структуры для таблица mafia_rate.Cards
CREATE TABLE IF NOT EXISTS `Cards` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `Title` varchar(10) NOT NULL,
  `IsActive` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Cards_ID_uindex` (`ID`),
  UNIQUE KEY `Cards_Title_uindex` (`Title`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.Cards: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `Cards` DISABLE KEYS */;
INSERT INTO `Cards` (`ID`, `Title`, `IsActive`) VALUES
	(1, 'Нейтральна', 0);
/*!40000 ALTER TABLE `Cards` ENABLE KEYS */;

-- Дамп структуры для таблица mafia_rate.City
CREATE TABLE IF NOT EXISTS `City` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(10) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `City_ID_uindex` (`ID`),
  UNIQUE KEY `City_Title_uindex` (`Title`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.City: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `City` DISABLE KEYS */;
INSERT INTO `City` (`ID`, `Title`) VALUES
	(1, 'Москва');
/*!40000 ALTER TABLE `City` ENABLE KEYS */;

-- Дамп структуры для таблица mafia_rate.Evenings
CREATE TABLE IF NOT EXISTS `Evenings` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `Date` datetime NOT NULL,
  `EndDate` datetime DEFAULT NULL,
  `ID_Location` int(10) NOT NULL,
  `ID_Initiator` int(10) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Evenings_ID_uindex` (`ID`),
  KEY `Evenings_Location_ID_fk` (`ID_Location`),
  KEY `Evenings_Members_ID_fk` (`ID_Initiator`),
  CONSTRAINT `Evenings_Location_ID_fk` FOREIGN KEY (`ID_Location`) REFERENCES `Location` (`ID`),
  CONSTRAINT `Evenings_Members_ID_fk` FOREIGN KEY (`ID_Initiator`) REFERENCES `Members` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.Evenings: ~4 rows (приблизительно)
/*!40000 ALTER TABLE `Evenings` DISABLE KEYS */;
INSERT INTO `Evenings` (`ID`, `Date`, `EndDate`, `ID_Location`, `ID_Initiator`) VALUES
	(3, '2017-12-04 18:19:13', '2017-12-04 19:02:18', 1, NULL),
	(4, '2017-12-05 19:01:39', '2017-12-04 19:02:21', 1, NULL),
	(5, '2018-02-02 03:19:46', NULL, 1, 1),
	(6, '2018-02-02 03:22:07', NULL, 1, 1);
/*!40000 ALTER TABLE `Evenings` ENABLE KEYS */;

-- Дамп структуры для таблица mafia_rate.Event
CREATE TABLE IF NOT EXISTS `Event` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.Event: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `Event` DISABLE KEYS */;
/*!40000 ALTER TABLE `Event` ENABLE KEYS */;

-- Дамп структуры для таблица mafia_rate.GameEvents
CREATE TABLE IF NOT EXISTS `GameEvents` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Games` int(11) NOT NULL,
  `ID_Events` int(11) NOT NULL,
  `ID_Init_Players` int(11) NOT NULL,
  `ID_Target_Players` int(11) NOT NULL,
  `Event_Number` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `GameEvents_Games_ID_fk` (`ID_Games`),
  KEY `GameEvents_Event_ID_fk` (`ID_Events`),
  KEY `GameEvents_Members_Init_ID_fk` (`ID_Init_Players`),
  KEY `GameEvents_Members_Target_ID_fk` (`ID_Target_Players`),
  CONSTRAINT `GameEvents_Event_ID_fk` FOREIGN KEY (`ID_Events`) REFERENCES `Event` (`ID`),
  CONSTRAINT `GameEvents_Games_ID_fk` FOREIGN KEY (`ID_Games`) REFERENCES `Games` (`ID`),
  CONSTRAINT `GameEvents_Members_Init_ID_fk` FOREIGN KEY (`ID_Init_Players`) REFERENCES `Members` (`ID`),
  CONSTRAINT `GameEvents_Members_Target_ID_fk` FOREIGN KEY (`ID_Target_Players`) REFERENCES `Members` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Дамп структуры для таблица mafia_rate.Games
CREATE TABLE IF NOT EXISTS `Games` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `IdHost` int(11) NOT NULL,
  `IdEvening` int(11) NOT NULL,
  `CourseCount` int(11) NOT NULL,
  `IsMafiaWin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Games_ID_uindex` (`ID`),
  KEY `Games_Members_ID_fk` (`IdHost`),
  KEY `Games_IdEvening_uindex` (`IdEvening`),
  CONSTRAINT `Games_Evenings_ID_fk` FOREIGN KEY (`IdEvening`) REFERENCES `Evenings` (`ID`),
  CONSTRAINT `Games_Members_ID_fk` FOREIGN KEY (`IdHost`) REFERENCES `Members` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.Games: ~3 rows (приблизительно)
/*!40000 ALTER TABLE `Games` DISABLE KEYS */;
INSERT INTO `Games` (`ID`, `IdHost`, `IdEvening`, `CourseCount`, `IsMafiaWin`) VALUES
	(1, 1, 3, 12, 1),
	(8, 1, 3, 1, 1),
	(11, 1, 4, 12, 1);
/*!40000 ALTER TABLE `Games` ENABLE KEYS */;

-- Дамп структуры для таблица mafia_rate.GamesPlayers
CREATE TABLE IF NOT EXISTS `GamesPlayers` (
  `ID_Player` int(11) NOT NULL,
  `ID_Games` int(11) NOT NULL,
  `ID_Card` int(11) NOT NULL,
  `ID_Role` int(11) NOT NULL,
  KEY `GamesPlayers_Games_ID_fk` (`ID_Games`),
  KEY `GamesPlayers_Roles_ID_fk` (`ID_Role`),
  KEY `GamesPlayers_Cards_ID_fk` (`ID_Card`),
  KEY `GamesPlayers_Members_ID_fk` (`ID_Player`),
  CONSTRAINT `GamesPlayers_Cards_ID_fk` FOREIGN KEY (`ID_Card`) REFERENCES `Cards` (`ID`),
  CONSTRAINT `GamesPlayers_Games_ID_fk` FOREIGN KEY (`ID_Games`) REFERENCES `Games` (`ID`),
  CONSTRAINT `GamesPlayers_Members_ID_fk` FOREIGN KEY (`ID_Player`) REFERENCES `Members` (`ID`),
  CONSTRAINT `GamesPlayers_Roles_ID_fk` FOREIGN KEY (`ID_Role`) REFERENCES `Roles` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.GamesPlayers: ~3 rows (приблизительно)
/*!40000 ALTER TABLE `GamesPlayers` DISABLE KEYS */;
INSERT INTO `GamesPlayers` (`ID_Player`, `ID_Games`, `ID_Card`, `ID_Role`) VALUES
	(1, 1, 1, 2),
	(1, 8, 1, 1),
	(1, 11, 1, 3);
/*!40000 ALTER TABLE `GamesPlayers` ENABLE KEYS */;

-- Дамп структуры для таблица mafia_rate.Inviters
CREATE TABLE IF NOT EXISTS `Inviters` (
  `ID_Member` int(10) NOT NULL,
  `ID_Inviter` int(10) NOT NULL,
  KEY `Inviters_Members_ID_fk_1` (`ID_Member`),
  KEY `Inviters_Members_ID_fk_2` (`ID_Inviter`),
  CONSTRAINT `Inviters_Members_ID_fk_1` FOREIGN KEY (`ID_Member`) REFERENCES `Members` (`ID`),
  CONSTRAINT `Inviters_Members_ID_fk_2` FOREIGN KEY (`ID_Inviter`) REFERENCES `Members` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.Inviters: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `Inviters` DISABLE KEYS */;
/*!40000 ALTER TABLE `Inviters` ENABLE KEYS */;

-- Дамп структуры для таблица mafia_rate.Location
CREATE TABLE IF NOT EXISTS `Location` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(15) NOT NULL,
  `ID_City` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Location_ID_uindex` (`ID`),
  UNIQUE KEY `Location_Title_uindex` (`Title`),
  KEY `Location_City_ID_fk` (`ID_City`),
  CONSTRAINT `Location_City_ID_fk` FOREIGN KEY (`ID_City`) REFERENCES `City` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.Location: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `Location` DISABLE KEYS */;
INSERT INTO `Location` (`ID`, `Title`, `ID_City`) VALUES
	(1, 'Зеленая Дверь', 1);
/*!40000 ALTER TABLE `Location` ENABLE KEYS */;

-- Дамп структуры для таблица mafia_rate.Members
CREATE TABLE IF NOT EXISTS `Members` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL DEFAULT '0',
  `IsHost` tinyint(1) NOT NULL DEFAULT '0',
  `Telephone` bigint(20) DEFAULT NULL,
  `IdTelegram` int(11) DEFAULT NULL,
  `NameTelegram` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Members_IdTelegram_uindex` (`IdTelegram`),
  UNIQUE KEY `Members_NameTelegram_uindex` (`NameTelegram`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.Members: ~10 rows (приблизительно)
/*!40000 ALTER TABLE `Members` DISABLE KEYS */;
INSERT INTO `Members` (`ID`, `Name`, `IsHost`, `Telephone`, `IdTelegram`, `NameTelegram`) VALUES
	(1, 'Михаил Солнцев', 1, 78001010, 193019697, NULL),
	(2, 'Михаил Ватутин', 1, 79999801929, 1, '@va2tin'),
	(11, 'Петр Масляков', 0, 7999, 2, ''),
	(12, 'Дмитрий Хабаров', 1, NULL, NULL, '@mrDarcky'),
	(13, 'Даниил Узвалок', 1, NULL, NULL, NULL),
	(14, 'Александр Редькин', 0, NULL, NULL, NULL),
	(15, 'Ибрагим Зубаилов', 0, NULL, NULL, NULL),
	(16, 'Дмитрий Факин ', 0, NULL, NULL, NULL),
	(17, 'Денис Инокеньтевич', 0, NULL, NULL, NULL),
	(18, 'Богдан Антонов', 1, NULL, 208204876, NULL);
/*!40000 ALTER TABLE `Members` ENABLE KEYS */;

-- Дамп структуры для таблица mafia_rate.Roles
CREATE TABLE IF NOT EXISTS `Roles` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `Name` varchar(15) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Roles_ID_uindex` (`ID`),
  UNIQUE KEY `Roles_Name_uindex` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы mafia_rate.Roles: ~3 rows (приблизительно)
/*!40000 ALTER TABLE `Roles` DISABLE KEYS */;
INSERT INTO `Roles` (`ID`, `Name`) VALUES
	(3, 'Коммисар'),
	(1, 'Мафия'),
	(2, 'Мирный житель');
/*!40000 ALTER TABLE `Roles` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

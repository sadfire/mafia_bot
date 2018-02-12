create table GameModes
(
	ID int(10) auto_increment
		primary key,
	Title varchar(20) not null,
	TitleEn varchar(20) not null,
	constraint GameModes_ID_uindex
		unique (ID),
	constraint GameModes_Title_uindex
		unique (Title)
)
;

UPDATE mafia_rate.GameModes SET Title = 'СуперРежим', TitleEn = 'Super' WHERE ID = 1;
UPDATE mafia_rate.GameModes SET Title = 'Новичковый набор', TitleEn = 'Beginner' WHERE ID = 2;
UPDATE mafia_rate.GameModes SET Title = 'Стандартный набор', TitleEn = 'Standart' WHERE ID = 3;
UPDATE mafia_rate.GameModes SET Title = 'Макендонская', TitleEn = 'Macedonia' WHERE ID = 4;
UPDATE mafia_rate.GameModes SET Title = 'Убийца', TitleEn = 'Killer' WHERE ID = 5;
UPDATE mafia_rate.GameModes SET Title = 'Поговорим?', TitleEn = 'LetsTalk' WHERE ID = 6;
UPDATE mafia_rate.GameModes SET Title = 'Якудза', TitleEn = 'Yakudza' WHERE ID = 7;
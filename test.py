import Evening as m

member_h = m.Member(0, "Михаил", 0)


evening = m.Evening(member_h)

for i in range(10):
    member_p = m.Member(i, "Иван", 0)
    member_p.name = member_p.name + str(i)
    evening.add_player(member_p)

game = evening.start_game()


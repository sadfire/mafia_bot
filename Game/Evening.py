from Game.Member import Member


class Evening:
    def __init__(self, host) -> None:
        super().__init__()
        self.members = {}
        self.hosts = [host]

    def add_member(self, member):
        if not isinstance(member, Member) or member.id in self.members.keys():
            return False

        self.members[member.id] = member
        return True

    def remove_member(self, member):
        if isinstance(member, Member):
            member = member.id

        self.members.pop(member)

    def is_ready(self):
        return len(self.members) > 2  # TODO More checks # TODO 2 only for debug

    def get_hosts_ids(self):
        return [host.id for host in self.hosts]
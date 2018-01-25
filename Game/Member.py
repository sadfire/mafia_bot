class Member:
    def __init__(self, id, name, is_host=False, phone_number=0, t_id=0) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.is_host = is_host
        self.phone_number = phone_number
        self.t_id = t_id

    def __str__(self):
        return self.name
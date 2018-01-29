from telegram import Message


class Provider:
    def __init__(self, t_id, send_method, edit_method) -> None:
        super().__init__()
        self.t_id = t_id
        self.send_method = send_method
        self.edit_method = edit_method
        self.keyboards = {}

    def send(self, text, reply_markup) -> Message:
        multi_page_message = reply_markup
        reply_markup = reply_markup.to_markup(0)

        message = self.send_method(chat_id=self.t_id, text=text, reply_markup=reply_markup)

        self.keyboards[message.message_id] = multi_page_message

        return message

    def edit(self, m_id, text, multi_page_kb) -> Message:
        if m_id in self.keyboards:
            page = self.keyboards[m_id].page
        else:
            page = 0

        self.keyboards[m_id] = multi_page_kb
        reply_markup = self.keyboards[m_id].to_markup(page)
        return self.send_method(chat_id=self.t_id,
                                message_id=m_id,
                                text=text,
                                reply_markup=reply_markup)

    def callback(self, bot, update, page):
        m_id = update.effective_message.message_id
        if m_id not in self.keyboards:
            raise ValueError

        self.edit_method(chat_id=self.t_id,
                         message_id=m_id,
                         reply_markup=self.keyboards[m_id].to_markup(page))

import logging


class Provider:
    @classmethod
    def process(cls, bot, update, callback_destinations):
        query, arguments = cls.get_arguments(update.callback_query.data)

        for callback_destination in callback_destinations:

            if query not in dir(callback_destination.__class__):
                continue

            result = cls._callback_provide(callback_destination, query, arguments, bot, update)
            if result is not None:
                return result

        return None

    @classmethod
    def get_arguments(cls, query):
        query, *arguments = query.split('.')

        if len(arguments) == 1:
            arguments = arguments[0]

        return query, arguments

    @classmethod
    def _callback_provide(cls, callback_destination, query, arguments, bot, update):
        if len(query) == 0:
            return

        try:
            callback = getattr(callback_destination, query)

            if (isinstance(arguments, list) and len(arguments) == 0) or arguments is None:
                return callback(bot, update)
            else:
                return callback(bot, update, arguments)

        except AttributeError as er:
            logging.warning(er)
            logging.warning("Callback error: ", query, arguments)

        return None


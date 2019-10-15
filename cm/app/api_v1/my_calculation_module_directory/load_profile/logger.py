class Logger:
    def __init__(self):
        self.messages = []
        self.message_types = []

    def add_information(self, information):
        self.messages.append(information)
        self.message_types.append("information")

    def add_warning(self, warning):
        self.messages.append(warning)
        self.message_types.append("warning")

    def add_error(self, error):
        self.messages.append(error)
        self.message_types.append("error")

    def string_report(self):
        log_string = ""
        for message, type_ in zip(self.messages, self.message_types):
            log_string += type_ + ": " + message + "    "
        return log_string

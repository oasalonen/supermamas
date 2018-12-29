import smtplib, ssl

class Emailer:
    __instance = None

    def __new__(cls, app=None):
        if not Emailer.__instance:
            Emailer.__instance = object.__new__(cls)
            Emailer.__instance.app = app
        return Emailer.__instance

    @property
    def sender(self):
        return self.__instance.app.config.get("MAIL_SENDER")

    @property
    def server(self):
        return self.__instance.app.config.get("MAIL_SERVER_ADDRESS")

    @property
    def port(self):
        return self.__instance.app.config.get("MAIL_SERVER_PORT")

    def send_message(self, receivers, message):
        with smtplib.SMTP(self.server, self.port) as server:
            for receiver in receivers:
                server.sendmail(self.sender, receiver, message.as_string())
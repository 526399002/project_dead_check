import re
import psutil
from sendmail import SendEmail
from var.dead_var import EmailMixIn
from var.global_var import log_settings, ExecuteMixin


class InspectProcessAlive(EmailMixIn, ExecuteMixin):
    def __init__(self, project, command, mail_body, recipients, executes=None):
        self.project = project
        self.command = command
        self.mail_body = mail_body
        self.recipients = recipients
        self.executes = executes

        self.send_mail = SendEmail()
        self.counts_send = 1
        self.current_error_send = 0
        self.logging = log_settings("log/process_alive.log")

    def main_inspect(self):
        is_running = False
        pattern = re.compile(self.command)
        for prc in psutil.process_iter():
            cmd = " ".join(prc.cmdline())
            if pattern.search(cmd):
                is_running = True
        if is_running:
            if self.error_is_send:
                self.ok_send()
        else:
            self.logging.warning("[{}] is not stop running!".format(self.project))
            self.error_send()
            self.operation()

import os
from utils.logger import Logger

log = Logger(__name__)

SEND_MAIL_BIN = "/auto/andatc/independent/build-scripts/1.0/bin/send_mail.pl"


class Mailer:

    def __init__(self, to_addr):
        self.from_addr = "n9k-sanity"
        self.to_addr = to_addr

    def send_mail(self, subject, output_file, option=""):
        cmd = "{0} --from {1} --to {2} --subject '{3}' --file {4} {5}".format(
            SEND_MAIL_BIN, self.from_addr, self.to_addr, subject, output_file, option)
        log.debug(cmd)
        os.system(cmd)

    def send_html_mail(self, subject, output_file):
        self.send_mail(subject, output_file, "--html")

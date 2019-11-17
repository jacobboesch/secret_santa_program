import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import secret_santa.config as config
import traceback
from secret_santa.response import ErrorException


class EmailSender():

    def __init__(self, to, subject, body, attachment=None, bc=None):
        self.to = to
        self.attachment = attachment
        self.message = MIMEMultipart()
        self.message["From"] = config.SENDER_EMAIL
        self.message["To"] = self.to
        self.message["Subject"] = subject
        self.bc = bc
        self.message.attach(MIMEText(body, "html"))
        if(attachment is not None):
            self._attach_file()

    def _attach_file(self):
        try:
            with open(self.attachment, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            file_name = os.path.basename(self.attachment)
            part.add_header(
                "Content-Disposition",
                "attachment; filename=" + file_name)
            self.message.attach(part)
        except Exception:
            traceback.print_exc()
            raise ErrorException("Unable to attach file to email", 500)

    def send(self):
        try:
            text = self.message.as_string()
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                                  config.SMTP_SERVER,
                                  config.PORT,
                                  context=context) as server:
                server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
                server.sendmail(config.SENDER_EMAIL, self.to, text)
        except Exception:
            traceback.print_exc()
            raise ErrorException(
                    "Unable to send email to {to}".format(to=self.to), 500)

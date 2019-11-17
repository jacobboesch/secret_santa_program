from secret_santa.util.email_sender import EmailSender
import secret_santa.config as config

with open(config.EMAIL_TEMPLATE) as file:
    body = file.read()
    with open(config.EMAIL_TEMPLATE_STYLE) as style_file:
        style = style_file.read()

sender = EmailSender(config.SENDER_EMAIL, "Test", body.format(name="Jacob", giftee_name="James", css=style))
sender.send()

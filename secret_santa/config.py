import os
SENDER_EMAIL = os.environ.get("SECRET_SANTA_SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SECRET_SANTA_SENDER_PASSWORD")
SMTP_SERVER = "smtp.mailtrap.io"
EMAIL_TEMPLATE = "secret_santa/templates/email_template.html"
EMAIL_TEMPLATE_STYLE = "secret_santa/templates/email_template.css"
PORT = 2525
EMAIL_SUBJECT = "Secret Santa"

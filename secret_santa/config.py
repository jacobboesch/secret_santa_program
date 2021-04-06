# Defines Global Constants
import os

CONNECTION_STRING = os.environ.get("SECRET_SANTA_DB_CONNECTION_STRING")
SENDER_EMAIL = "15f9412f7a0392" #os.environ.get("SECRET_SANTA_SENDER_EMAIL")
SENDER_PASSWORD = "958db6506297b5"#os.environ.get("SECRET_SANTA_SENDER_PASSWORD")
SMTP_SERVER = "smtp.mailtrap.io"
EMAIL_TEMPLATE = "secret_santa/templates/email_template.html"
EMAIL_TEMPLATE_STYLE = "secret_santa/templates/email_template.css"
PORT = 2525
EMAIL_SUBJECT = "Secret Santa"
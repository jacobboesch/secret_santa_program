# Defines Global Constants
import os

CONNECTION_STRING = os.environ.get("SECRET_SANTA_DB_CONNECTION_STRING")
SENDER_EMAIL = os.environ.get("SECRET_SANTA_SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SECRET_SANTA_SENDER_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
EMAIL_TEMPLATE = "secret_santa/templates/email_template.html"
EMAIL_TEMPLATE_STYLE = "secret_santa/templates/email_template.css"
PORT = 465
EMAIL_SUBJECT = "NEW AND FINAL Secret Santa Results"
from secret_santa.response.success_response import SuccessResponse
from secret_santa.response.error_response import ErrorResponse
from secret_santa.response.error_exception import ErrorException
from secret_santa.util.email_sender import EmailSender
import secret_santa.config as config
import traceback
import threading


# used to send the emails in parallel
class EmailParticipantThread(threading.Thread):
    def __init__(self, selection, body, style):
        threading.Thread.__init__(self)
        self.selection = selection
        self.body = body
        self.style = style

    def run(self):
        sender = EmailSender(
            self.selection["email"],
            config.EMAIL_SUBJECT,
            self.body.format(
                css=self.style,
                name=self.selection["name"],
                giftee_name=self.selection["gifteeName"]
            )
        )
        sender.send()


class EmailService():

    def _get_file_contents(self, file_path):
        body = None
        try:
            template = open(file_path, "rt")
            body = template.read()
            template.close()
        except Exception:
            raise ErrorException("Error opening email template", 500)
        return body

    # email participants based on the selections (participant with selected giftee)
    def email_participants(self, selections):
        body = self._get_file_contents(config.EMAIL_TEMPLATE)
        style = self._get_file_contents(config.EMAIL_TEMPLATE_STYLE)
        try:
            threads = []
            for selection in selections:
                thread = EmailParticipantThread(selection, body, style)
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
        except ErrorException as e:
            return ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            return ErrorResponse(500, "Unknown Error")

        return SuccessResponse("Success")

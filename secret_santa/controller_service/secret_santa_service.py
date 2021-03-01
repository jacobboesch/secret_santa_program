from secret_santa.repository import ParticipantRepository
from secret_santa.response import SuccessResponse, ErrorResponse
from secret_santa.response import ErrorException
from secret_santa.util.email_sender import EmailSender
import traceback
import secret_santa.config as config
import multiprocessing as mp


class SecretSantaService():
    repo = None

    def __init__(self):
        self.repo = ParticipantRepository()

    # start the secret santa program
    # returns a response object
    def start(self):
        try:
            self.repo.update_giftees()
            self._email_participants()
        except ErrorException as e:
            return ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            return ErrorResponse(500, "Unknown Error")

        return SuccessResponse("Success")


    def _convert_participants_to_dict(self,list_participants):
        participant_dictionary = dict()
        for participant in list_participants:
            participant_dictionary[participant.id] = participant
        return participant_dictionary
    
    def _email_participant(self, participant_dict, participant, body, style):
        giftee = participant_dict[participant.giftee]
        sender = EmailSender(
            giftee.email,
            config.EMAIL_SUBJECT,
            body.format(
                css=style,
                name=participant.name,
                giftee_name=giftee.name))
        sender.send()


    def _email_participants(self):
        body = self._get_file_contents(config.EMAIL_TEMPLATE)
        style = self._get_file_contents(config.EMAIL_TEMPLATE_STYLE)
        participants = self.repo.retrieve_all_with_giftee()
        participant_dict = self._convert_participants_to_dict(participants)
        try:
            # email each participant in parallel upto the max cpu count
            pool = mp.Pool(mp.cpu_count())
            [pool.apply(
                self._email_participant,
                args=(
                    participant_dict,
                    participant,
                    body,
                    style)
            ) for participant in participants]
        except ErrorException as e:
            raise e
        except Exception:
            traceback.print_exc()
            raise ErrorException("Unknown error", 500)

    def _get_file_contents(self, file_path):
        body = None
        try:
            template = open(file_path, "rt")
            body = template.read()
            template.close()
        except Exception:
            raise ErrorException("Error opening email template", 500)
        return body

from secret_santa.repository import ParticipantRepository
from secret_santa.response import SuccessResponse, ErrorResponse
from secret_santa.response import ErrorException
from secret_santa.util.email_sender import EmailSender
import traceback
import secret_santa.config as config


class SecretSantaService():

    def __init__(self):
        self.repo = ParticipantRepository()

    # start the secret santa program
    # returns a response object
    def start(self):
        try:
            self._reset_giftees_and_selected()
            self._select_giftees()
            self._email_participants()
        except ErrorException as e:
            return ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            return ErrorResponse(500, "Unknown Error")

        return SuccessResponse("Success")

    def _reset_giftees_and_selected(self):
        self.repo.reset_giftees()
        self.repo.unselect_all()

    def _select_giftees(self):
        # Change number after statistical anyalysis, needs to be the
        # maximum number of times we attempt this algorithm before
        # stating that the program failed
        max_error_count = 200
        error_count = 0
        num_people = self.repo.num_people_without_giftee()
        while(num_people > 0):
            ###
            # the house id is the id of the househod that has the most number
            # of people wihout a giftee
            ###
            house_id = self.repo \
                .retrieve_most_populated_household_id_without_giftee()
            current_person = self.repo \
                .retrieve_by_household_without_giftee(house_id)
            giftee = self.repo \
                .retrieve_random_not_selected_not_in_household(house_id)
            if (giftee is None):
                error_count = error_count + 1
                self._reset_giftees_and_selected()
                if(error_count >= max_error_count):
                    raise ErrorException("Failed to select giftees", 500)
            else:
                current_person.giftee = giftee.id
                giftee.is_selected = True
                self.repo.update(current_person)
                self.repo.update(giftee)
            num_people = self.repo.num_people_without_giftee()

    def _email_participants(self):
        body = self._get_file_contents(config.EMAIL_TEMPLATE)
        style = self._get_file_contents(config.EMAIL_TEMPLATE_STYLE)
        participants = self.repo.retrieve_all_with_giftee()
        try:
            for participant in participants:
                giftee = self.repo.retrieve_by_id(participant.giftee)
                sender = EmailSender(
                    participant.email,
                    config.EMAIL_SUBJECT,
                    body.format(
                        css=style,
                        name=participant.name,
                        giftee_name=giftee.name))
                sender.send()
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

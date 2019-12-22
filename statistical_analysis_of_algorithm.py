###
# This is designed to find the probability of the algorithm working or not
# TODO Convert this prototype program into a proper endpoint
###

from secret_santa.database import init_db, Base, engine
from secret_santa.repository import ParticipantRepository
from secret_santa.model import Participant


def main(sampleSize=100):
    i = 0
    fail_count = 0
    drop_database()
    repo = ParticipantRepository()
    add_test_data(repo)
    while(i < sampleSize):
        reset_columns(repo)
        try:
            algorithm(repo)
        except Exception:
            fail_count = fail_count + 1
        i = i + 1
    prob_fail = fail_count / sampleSize
    prob_success = (sampleSize - fail_count) / sampleSize
    print("Probability of failure: ", prob_fail)
    print("Probability of success: ", prob_success)


def drop_database():
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    init_db()


def reset_columns(repo):
    repo.reset_giftees()
    repo.unselect_all()


def algorithm(repo):
    num_people = repo.num_people_without_giftee()
    while(num_people > 0):
        ###
        # the house id is the id of the househod that has the most number of
        # people wihout a giftee
        ###
        house_id = repo.retrieve_most_populated_household_id_without_giftee()
        current_person = repo.retrieve_by_household_without_giftee(house_id)
        giftee = repo.retrieve_random_not_selected_not_in_household(house_id)
        if (giftee is None
                or current_person.name == "Grandma" and giftee.name == "Jacob"
                or current_person.name == "Grandpa" and giftee.name == "Jacob"
                or current_person.name == "Bill" and giftee.name == "Grandpa"
                or current_person.name == "Marianne" and giftee.name == "Bill"
                or current_person.name == "Jeremy" and giftee.name == "Candra"
                or current_person.name == "Julianne" and giftee.name == "Grandma"
                or current_person.name == "Candra" and giftee.name == "Jeremy"
                or current_person.name == "Grandpa" and giftee.name == "Marianne"
                or current_person.name == "Grandma" and giftee.name == "Ange"):
            raise Exception("Failed to find a giftee")
        current_person.giftee = giftee.id
        giftee.is_selected = True
        repo.update(current_person)
        repo.update(giftee)
        num_people = repo.num_people_without_giftee()
    displayTable(repo)


def add_test_data(repo):
    repo.create(Participant("Jacob", 1, "test"))
    repo.create(Participant("Marianne", 1, "test"))
    repo.create(Participant("Jeremy", 1, "test"))
    repo.create(Participant("Grandma", 2, "test"))
    repo.create(Participant("Grandpa", 2, "test"))
    repo.create(Participant("Bill", 3, "test"))
    repo.create(Participant("Candra", 3, "test"))
    repo.create(Participant("Jessica", 4, "test"))
    repo.create(Participant("James", 4, "test"))
    repo.create(Participant("Juileanne", 4, "test"))
    repo.create(Participant("Ange", 4, "test"))


def displayTable(repo):
    participants = repo.retrieve_all()
    print("|id \t name \t household \t giftee \n")
    for p in participants:
        print(
            "| {id} \t| {name} |\t| {household} |\t| {giftee} |\t|".format(
                id=p.id,
                name=p.name,
                household=p.household,
                giftee=p.giftee)
        )

main(100)

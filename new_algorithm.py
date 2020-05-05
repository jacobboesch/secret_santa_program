import sqlalchemy
from sqlalchemy import create_engine
import itertools
import random
import time
import traceback

engine = create_engine('sqlite:///secret_santa.db')

def algorithm():
    start_time = time.time()
    participants = set()
    taken_giftees = set()
    res = []
    options = []
    peoples = []
    with engine.connect() as connect:
        result_set = connect.execute('SELECT P.id AS id, COUNT(G.id) AS num_possible_giftees, group_concat(G.id) AS possible_giftees FROM participants AS P, participants AS G WHERE P.id != G.id AND P.household != G.household AND P.giftee != G.id GROUP BY P.id ORDER BY num_possible_giftees ASC')
        
        for row in result_set:
            possible_giftees = set(map(int,row.possible_giftees.split(",")))
            options.append((row.id, possible_giftees))
    
    i = 0
    fail_count = 0
    sampleSize = 100
    
    while(i < sampleSize):
        try:
            res.clear()
            participants.clear()
            taken_giftees.clear()
           
            for option in options:
                selected_giftee = None
                possible_giftees = list(option[1] - taken_giftees)
                if(len(possible_giftees) == 0):
                    raise Exception("Failed to find a giftee")
                random.shuffle(possible_giftees)
                res.append((option[0], possible_giftees[0]))
                taken_giftees.add(possible_giftees[0])

            if(len(res) != 11):
                raise Exception("Failed")
        except:
            fail_count += 1
        i += 1
    
    prob_fail = fail_count / sampleSize
    prob_success = (sampleSize - fail_count) / sampleSize
    print("Probability of failure: ", prob_fail)
    print("Probability of success: ", prob_success)
    print("Time elapsed", time.time() - start_time)

algorithm()
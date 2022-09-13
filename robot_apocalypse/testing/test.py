#!/usr/bin/python3
import json, requests

if __name__=="__main__":
    i_choice = int(input("1 - add survivor, 2 - list survivors, 3 - flag survivor, 4 - update gps coordinates, 5 - list robots"))
    if i_choice==1:
        # add survivor
        d_questions = {}
        d_questions["name"] = "(just name string)"
        d_questions["age"] = "(integer value)"
        d_questions["gender"] = "(string value)"
        d_questions["id_number"] = "(to be used to identify survivor later on)"
        d_questions["latitude"] = "(decimal value)"
        d_questions["longitude"] = "(decimal value)"
        d_questions["inventory"] = "(example - apples|1||bullets|100)"
        for sk in d_questions:
            s_detail = d_questions[sk]
            d_questions[sk] = input(f"{sk} - {s_detail}")
        # end of question loop
        s_url = "http://localhost:8000/add"
        rp = requests.post(s_url, d_questions)
        print(rp.status_code, rp.text)
    elif i_choice==2:
        # list survivors
        s_url = "http://localhost:8000/survivors"
        rp = requests.get(s_url)
        print(rp.status_code, rp.text)
    elif i_choice==3:
        # flag survivor
        d_questions = {"reporting": "(ID number of reporting survivor)", "infected": "(ID number of infected survivor)"}
        for sk in d_questions:
            s_detail = d_questions[sk]
            d_questions[sk] = input(f"{sk} - {s_detail}")
        # end of question loop
        s_url = "http://localhost:8000/flag"
        rp = requests.post(s_url, d_questions)
        print(rp.status_code, rp.text)
    elif i_choice==4:
        # gps coordinates
        d_questions = {"id_number": "(to be used to identify survivor)", "latitude": "(decimal value)", "longitude": "(decimal value)"}
        for sk in d_questions:
            s_detail = d_questions[sk]
            d_questions[sk] = input(f"{sk} - {s_detail}")
        # end of question loop
        s_url = "http://localhost:8000/gps"
        rp = requests.post(s_url, d_questions)
        print(rp.status_code, rp.text)
    else:
        # list robots
        s_url = "http://localhost:8000/robots"
        rp = requests.get(s_url)
        print(rp.status_code, rp.text)
# end of checking if __main__

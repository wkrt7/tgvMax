import requests
import json

def generate_url(origine, destination, date):
    d = date.split("/")
    url = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=tgvmax"
    url += "&refine.destination=" + destination
    url += "&refine.origine=" + origine
    url += "&refine.date=" + d[2] + "%2F" + d[1] + "%2F" + d[0]
    # url += "&apikey=" + api_key
    return url

u = generate_url("LILLE+EUROPE","PARIS+(intramuros)", "15/10/2017")
r = requests.get(u)

if r:
    body = r.json()
    for rec in body["records"]:
        if rec["fields"]["od_happy_card"] == "OUI":
            print("date : " + rec["fields"]["date"])
            print("heure de départ : " + rec["fields"]["heure_depart"])
            print("-------------\n")
else:
    print("ERROR")

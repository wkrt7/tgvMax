#!/usr/bin/env python3
import requests
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from CONFIG import *

LILLE = ["LILLE+EUROPE", "LILLE+FLANDRES"]
PARIS = ["PARIS+(intramuros)"]
DATE = "15/10/2017"
AFTER_HOUR = 12

def get_records(origine, destination, date):
    d = date.split("/")
    url = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=tgvmax"
    url += "&refine.destination=" + destination
    url += "&refine.origine=" + origine
    url += "&refine.date=" + d[2] + "%2F" + d[1] + "%2F" + d[0]
    # url += "&apikey=" + api_key
    r = requests.get(url)

    if r:
        body = r.json()
        return body["records"]
    else:
        raise requests.RequestException


def get_happy_card(records):
    happy_card = []
    for rec in records:
        if rec["fields"]["od_happy_card"] == "OUI":
            happy_card.append(rec["fields"])
    return happy_card

def is_interresting(record, after_hour):
    hour = record["heure_depart"].split(":")[0]
    hour = int(hour)
    if hour >= after_hour:
        return True
    else:
        return False


def createMsg(subject, txt):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To']   = EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(txt))
    return msg

def sendmail(msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL, EMAIL, text)
    server.quit()

def main():
    happy = []
    msg = ""
    for l in LILLE:
        rec = get_records(l, PARIS[0], DATE)
        happy.append(get_happy_card(rec))

    flat = [val for sublist in happy for val in sublist]

    for r in flat:
        if is_interresting(r, AFTER_HOUR):
            msg += "De " + r["origine"]
            msg += " le "
            msg += r["date"]
            msg += " à "
            msg += r["heure_depart"]
            msg += "h\n-------\n"

    if msg:
        sendmail(createMsg("[TGVMAX] Nouvel Horaire", msg))
        print("Message envoyé : " + msg)

if __name__ == '__main__':
    main()

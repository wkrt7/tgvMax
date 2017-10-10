from datetime import date
from datetime import timedelta
from datetime import datetime

import sncf_tgvmax as tgv

WEEK = {
"monday" 	: 0,
"tuesday" 	: 1,
"wednesday"	: 2,
"thursday" 	: 3,
"friday"  	: 4,
"saturday"  : 5,
"sunday"	: 6
}

# input : 0 = 'monday'
# return the dates within a timeslot of 30 days for a given day
# format of the dates in output : DD/MM/YYYY
def get_dates(weekday):
	if type(weekday) == str:
		wd = WEEK[weekday.lower()]
		return(get_dates(wd))
	today = date.today()
	res = []
	cpt = today
	while(cpt <= today + timedelta(days=30)):
		if cpt.weekday() == weekday:
			res.append(cpt.strftime("%d/%m/%Y"))
		cpt += timedelta(days=1)
	return res

if __name__ == "__main__":
	for d in get_dates("sunday"):
		print("reaching server for date : %s" %(d))
		rec = tgv.get_records(tgv.LILLE[0], tgv.PARIS[0], d))

import csv
from datetime import datetime

csvfilename = 'test.csv'

def write_time_to_csv(csvfilename):
    
    dtnow = datetime.now(tz = datetime.now().astimezone().tzinfo).isoformat(timespec='milliseconds')

    with open(csvfilename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([dtnow])



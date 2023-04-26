import csv
from datetime import datetime, timedelta
import re 
csvfilename = 'test.csv'

def write_time_to_csv(csvfilename):
    
    dtnow = datetime.now(tz = datetime.now().astimezone().tzinfo).isoformat(timespec='milliseconds')

    with open(csvfilename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([dtnow])
def average_order_time(file_name):
        with open (file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            for line in csv_reader:
                if (csv_reader.line_num % 2 == 0):
                    time_string =''.join(line)
                    # how to convert time_string to int? when it looks like the follwing: 2023-04-20T09:44:33.793+02:00
                    s = time_string
                    dt = datetime.fromisoformat(s)
                    year, month, day = dt.year, dt.month, dt.day
                    hour, minute, second = dt.hour, dt.minute, dt.second
                    timezone_offset = int(re.search(r"[-+]\d{2}:\d{2}$", s).group().replace(":", ""))
                    s = time_string
                    dt = datetime.fromisoformat(s)
                    unix_time = int(dt.timestamp())
                    print(unix_time)                 


if __name__ == '__main__':
    average_order_time(csvfilename)


import csv
from datetime import datetime, timedelta
import re 
import pandas as pd
csvfilename = 'test_copy.csv'

def write_time_to_csv(csvfilename):
    
    dtnow = datetime.now(tz = datetime.now().astimezone().tzinfo).isoformat(timespec='milliseconds')

    with open(csvfilename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([dtnow])

def average_order_time(file_name):
    
    #df = pd.read_csv(file_name, header=None, skiprows=[0], usecols=[0], names=['start', 'end'])
    #df['start'] = pd.to_datetime(df['start'], format='%Y-%m-%dT%H:%M:%S.%f%z')
    #df['end'] = pd.to_datetime(df['end'], format='%Y-%m-%dT%H:%M:%S.%f%z')
    #df['diff'] = df['end'] - df['start']
    #print(df['diff'].mean())

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name, header=None, skiprows=[0], usecols=[0], names=['time'])

    # Convert the column of interest to a datetime type
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%dT%H:%M:%S.%f%z')

    # Calculate the time differences between consecutive rows
    df['time_diff'] = df['time'] - df['time'].shift(periods=1)

    print(df['time_diff'])
    print(df['time_diff'].mean())

if __name__ == '__main__':
    average_order_time(csvfilename)


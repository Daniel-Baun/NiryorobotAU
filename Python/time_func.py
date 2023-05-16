import csv
from datetime import datetime, timedelta
import re 
import pandas as pd
import matplotlib.pyplot as plt

csvfilename = 'test_copy.csv'

def write_time_to_csv(csvfilename):
    
    dtnow = datetime.now(tz = datetime.now().astimezone().tzinfo).isoformat(timespec='milliseconds')

    with open(csvfilename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([dtnow])

def average_order_time(file_name):
    
    timestamps = []
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            timestamp = datetime.fromisoformat(row[0])
            timestamps.append(timestamp)

    mean_times = []
    for i in range(1, len(timestamps), 2):
        time_diff = timestamps[i] - timestamps[i-1]
        mean_times.append(time_diff.total_seconds())

    return mean_times
    #mean_time = sum(time_differences)/len(time_differences)

def plot_mean_times(mean_times):
    if mean_times:
        plt.figure(figsize=(8,6))
        plt.plot(mean_times, marker='o')
        plt.axhline(y=sum(mean_times)/len(mean_times), color='r', linestyle='--', label='Mean time for all orders')
        plt.xlabel('Order number')
        plt.ylabel('Time (seconds)')
        plt.title('Time to process orders')
        plt.legend()
        plt.grid(True)
        plt.show()

def plot_mean_times_line(mean_times):
    if mean_times:
        timestamps = range(1, len(mean_times)+1)
        plt.figure(figsize=(8,6))
        plt.plot(timestamps, mean_times, marker='o')
        plt.axhline(y=sum(mean_times)/len(mean_times), color='r', linestyle='--', label='Mean time for all orders')
        plt.xlabel('Order number')
        plt.ylabel('Time (seconds)')
        plt.title('Time to process orders')
        plt.legend()
        plt.grid(True)
        plt.show()

def print_mean_times(mean_times):
    if mean_times:
        for i, mean_time in enumerate(mean_times, start=1):
            print(f'Mean time {i}: {mean_time} seconds')
        print(f'Mean time for all orders: {sum(mean_times)/len(mean_times)} seconds')

if __name__ == '__main__':
    mean_times = average_order_time(csvfilename)
    plot_mean_times_line(mean_times)
    #average_order_time(csvfilename)


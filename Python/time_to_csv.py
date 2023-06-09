import csv
from datetime import datetime, timedelta
import re 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
        time_diff_seconds = time_diff.total_seconds()
        if time_diff_seconds <= 100:
            mean_times.append(time_diff_seconds)

    return mean_times
    #mean_time = sum(time_differences)/len(time_differences)

def calculate_standard_deviation(mean_times):
    if mean_times:
        return np.std(mean_times)

def plot_mean_times_line(mean_times, iterations):
    if mean_times:
        timestamps = range(1, len(mean_times) + 1)
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, mean_times, marker='o')
        plt.axhline(y=np.mean(mean_times), color='r', linestyle='--', label='Mean time')
        plt.xlabel('Order number')
        plt.ylabel('Time (seconds)')
        plt.title('Time to process orders')
        plt.grid(True)
        mean_time_text = np.mean(mean_times)
        std_dev_text = calculate_standard_deviation(mean_times)
        plt.axhline(y=mean_time_text + std_dev_text, color='g', linestyle='dashdot', label='Mean time ± standard deviation')
        plt.axhline(y=mean_time_text - std_dev_text, color='g', linestyle='dashdot')
        # Add vertical lines at every 25 x-axis interval
        for i, iteration in enumerate(iterations, 1):
            plt.axvline(x=iteration, color='b', linestyle=':', label=f'Version {i+1}')
            plt.text(iteration+3, np.max(mean_times)-40, f'Version {i+1}', rotation=90, va='bottom')

        plt.text(0, mean_time_text+5, f'Mean time: {mean_time_text:.2f} sec', color='r')
        plt.text(0, mean_time_text+4 + std_dev_text, f'Mean time + std deviation: {mean_time_text + std_dev_text:.2f} sec', color='g')
        plt.text(0, mean_time_text-5 - std_dev_text, f'Mean time - std deviation: {mean_time_text - std_dev_text:.2f} sec', color='g')
        plt.legend()
        plt.show()




if __name__ == '__main__':
    iterations = [20, 60, 110]  # Example iteration numbers
    mean_times = average_order_time(csvfilename)
    plot_mean_times_line(mean_times, iterations)


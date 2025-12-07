#!/usr/bin/env python3

import cgitb
cgitb.enable()

import csv
import sys
import os
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

print("Content-Type: text/html; charset=utf-8")
print("") 
print("<html><body>")

def create_graph():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    
    csv_path = os.path.join(parent_dir, 'sample.csv')
    output_path = os.path.join(parent_dir, 'monitor_graph.png')

    if not os.path.exists(csv_path):
        print(f"<h3>Error: CSV file not found at: {csv_path}</h3>")
        csv_path = os.path.join(base_dir, 'sample.csv')
        if not os.path.exists(csv_path):
            return False

    timestamps = []
    temperatures = []
    humidities = []

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 3: continue
                try:
                    dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    temp = float(row[1])
                    hum = float(row[2])
                    timestamps.append(dt)
                    temperatures.append(temp)
                    humidities.append(hum)
                except ValueError:
                    continue
    except Exception as e:
        print(f"<h3>File Read Error: {e}</h3>")
        return False

    if not timestamps:
        print("<h3>No data found in CSV.</h3>")
        return False
        
    latest_time = max(timestamps)
    start_time = latest_time - timedelta(hours=1)
    
    plot_times = []
    plot_temps = []
    plot_hums = []

    for t, temp, hum in zip(timestamps, temperatures, humidities):
        if t >= start_time:
            plot_times.append(t)
            plot_temps.append(temp)
            plot_hums.append(hum)

    if not plot_times:
        print("<h3>No data in the last 1 hour.</h3>")
        return False

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color_temp = 'green'
    ax1.set_xlabel('Time (HH:MM)')
    ax1.set_ylabel('Temperature (C)', color=color_temp)
    ax1.plot(plot_times, plot_temps, color=color_temp, label='Temperature')
    ax1.tick_params(axis='y', labelcolor=color_temp)
    ax1.set_ylim(0, 40)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    ax2 = ax1.twinx()
    color_hum = 'blue'
    ax2.set_ylabel('Humidity (%)', color=color_hum)
    ax2.plot(plot_times, plot_hums, color=color_hum, label='Humidity')
    ax2.tick_params(axis='y', labelcolor=color_hum)
    ax2.set_ylim(0, 100)

    plt.title(f"Environment Monitor (Latest 1h from {latest_time})")
    plt.grid(True)
    fig.tight_layout()

    try:
        plt.savefig(output_path)
        plt.close()
    except Exception as e:
        print(f"<h3>Save Error: {e}</h3>")
        return False
    
    return True

if __name__ == "__main__":
    success = create_graph()

    if success:
        print('<h3>Graph Updated! Redirecting...</h3>')
        print('<meta http-equiv="refresh" content="0;url=../index.html">')
    else:
        print('<h3>Update Failed. Please check the errors above.</h3>')
        print('<a href="../index.html">Back to Home</a>')

    print("</body></html>")

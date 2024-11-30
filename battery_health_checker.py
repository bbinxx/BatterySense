import psutil
import subprocess
import tkinter as tk
from tkinter import ttk
import threading
import time

# Global variables for average health calculation
battery_health_values = []

# Function to get battery information
def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return {
            "percent": battery.percent,
            "plugged_in": battery.power_plugged,
            "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "N/A"
        }
    else:
        return None

# Function to get battery health (Windows-specific)
def get_battery_health():
    try:
        # Retrieve design capacity
        design_capacity = subprocess.check_output(
            ['wmic', 'path', 'Win32_Battery', 'get', 'DesignCapacity'],
            universal_newlines=True
        ).strip().split("\n")[1].strip()

        # Retrieve full charge capacity
        full_charge_capacity = subprocess.check_output(
            ['wmic', 'path', 'Win32_Battery', 'get', 'FullChargeCapacity'],
            universal_newlines=True
        ).strip().split("\n")[1].strip()

        if design_capacity and full_charge_capacity:
            # Calculate battery health as a percentage
            health_percent = (int(full_charge_capacity) / int(design_capacity)) * 100
            return round(health_percent, 2)
        else:
            return None
    except Exception as e:
        return None

# Function to calculate average battery health
def calculate_average_health():
    if battery_health_values:
        return round(sum(battery_health_values) / len(battery_health_values), 2)
    return "N/A"

# Function to update battery information in real-time
def update_battery_info():
    while True:
        battery_info = get_battery_info()
        health = get_battery_health()

        if battery_info:
            # Append health value for average calculation
            if health:
                battery_health_values.append(health)
                # Limit stored health values for performance
                if len(battery_health_values) > 50:
                    battery_health_values.pop(0)

            # Update battery status on the UI
            plugged_in_status = "Yes" if battery_info["plugged_in"] else "No"
            time_left = battery_info["time_left"] if battery_info["time_left"] != "N/A" else "Calculating..."
            average_health = calculate_average_health()

            battery_status_label.config(
                text=f"Battery Percentage: {battery_info['percent']}%\n"
                     f"Plugged In: {plugged_in_status}\n"
                     f"Time Remaining: {time_left}\n"
                     f"Current Health: {health if health else 'N/A'}%\n"
                     f"Average Health: {average_health}%"
            )
        else:
            battery_status_label.config(
                text="Unable to retrieve battery information."
            )
        time.sleep(5)  # Refresh every 5 seconds

# Main GUI
root = tk.Tk()
root.title("BatterySense")
root.geometry("400x300")
root.resizable(False, False)

# Styling
style = ttk.Style(root)
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 10))

# Title Label
title_label = ttk.Label(root, text="BatterySense", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Battery Status Label
battery_status_label = ttk.Label(root, text="Fetching battery data...", justify="left")
battery_status_label.pack(pady=20)

# Exit Button
exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=10)

# Start the real-time update thread
thread = threading.Thread(target=update_battery_info, daemon=True)
thread.start()

# Run the app
root.mainloop()

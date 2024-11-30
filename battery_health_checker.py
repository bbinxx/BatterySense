import psutil
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
            return "N/A"
    except Exception as e:
        return str(e)

# Function to display battery information in the GUI
def show_battery_info():
    battery_info = get_battery_info()
    health = get_battery_health()

    if battery_info:
        plugged_in_status = "Yes" if battery_info["plugged_in"] else "No"
        time_left = battery_info["time_left"] if battery_info["time_left"] != "N/A" else "Calculating..."
        
        # Update the information on the GUI
        battery_status_label.config(
            text=f"Battery Percentage: {battery_info['percent']}%\n"
                 f"Plugged In: {plugged_in_status}\n"
                 f"Time Remaining: {time_left}\n"
                 f"Battery Health: {health}%"
        )
    else:
        messagebox.showerror("Error", "Battery information not available!")

# Main GUI
root = tk.Tk()
root.title("Battery Health Checker")
root.geometry("400x300")
root.resizable(False, False)

# Styling
style = ttk.Style(root)
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 10))

# Title Label
title_label = ttk.Label(root, text="Battery Health Checker", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Battery Status Label
battery_status_label = ttk.Label(root, text="Press the button to check battery status.", justify="left")
battery_status_label.pack(pady=20)

# Check Status Button
check_button = ttk.Button(root, text="Check Battery Status", command=show_battery_info)
check_button.pack(pady=10)

# Exit Button
exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=10)

# Run the app
root.mainloop()

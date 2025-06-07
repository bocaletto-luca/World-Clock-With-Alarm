# Software Name: World Clock With Alarm
# Author: Bocaletto Luca
# License: GPLv3

import tkinter as tk
from tkinter import ttk, messagebox
import pytz
from datetime import datetime
import threading
import winsound

# Function to display the selected time for the chosen time zone
def show_selected_time():
    selection = countries_combobox.get()
    if selection:
        try:
            # Get the selected time zone and the current time in that zone
            time_zone = pytz.timezone(selection)
            current_time = datetime.now(time_zone)
            
            # Update the time label with the current time in the selected time zone
            time_label.config(text=f"Time in {selection}: {current_time.strftime('%H:%M:%S')}")
        except pytz.exceptions.UnknownTimeZoneError:
            # Display an error message if the time zone is unknown
            time_label.config(text=f"Unknown time zone for {selection}")
    
    # Schedule the function to run again after 1 second
    app.after(1000, show_selected_time)

# Function to set an alarm
def set_alarm():
    selected_time = alarm_time_entry.get()
    if not selected_time:
        return

    # Get the current time
    current_time = datetime.now()

    # Extract the hour and minute from the selected alarm time
    alarm_hour, alarm_minute = map(int, selected_time.split(":"))

    # Create a datetime object for the alarm time
    alarm_time = current_time.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

    selection = countries_combobox.get()
    if selection:
        try:
            # Get the selected time zone
            time_zone = pytz.timezone(selection)

            # Localize the alarm time to the selected time zone
            alarm_time = time_zone.localize(alarm_time)

            # Calculate the time difference between the alarm time and current time
            difference = alarm_time - datetime.now(time_zone)

            if difference.total_seconds() > 0:
                # Function to play the alarm sound and show a message
                def play_alarm():
                    winsound.Beep(500, 1000)
                    messagebox.showinfo("Alarm Clock", f"Alarm clock set for {selected_time} in {selection}")

                # Schedule the alarm function to run after the time difference
                threading.Timer(difference.total_seconds(), play_alarm).start()

                # Display a success message with green text
                alarm_status_label.config(text=f"Alarm clock set for {selected_time} in {selection}", fg="green")
            else:
                # Display a message in red text indicating that the selected time has already passed
                alarm_status_label.config(text="The selected time has already passed.", fg="red")
        except pytz.exceptions.UnknownTimeZoneError:
            # Display an error message in red text for an unknown time zone
            alarm_status_label.config(text=f"Unknown time zone for {selection}", fg="red")
    else:
        # Display a message in red text indicating that no time zone was selected
        alarm_status_label.config(text="Please select a time zone", fg="red")

# Create the main application window 
app = tk.Tk()
app.title("World Clock With Alarm")

# Create and configure UI elements 
title_label = tk.Label(app, text="World Clock With Alarm", font=("Helvetica", 16))
title_label.pack(pady=10)

lbl_countries = tk.Label(app, text="Select a country:")
lbl_countries.pack()

# Populate the time zone selection combobox with available time zones
countries = pytz.all_timezones
countries_combobox = ttk.Combobox(app, values=countries)
countries_combobox.pack()

show_selected_button = tk.Button(app, text="Show Time", command=show_selected_time)
show_selected_button.pack()

time_label = tk.Label(app, text="")
time_label.pack()

set_alarm_button = tk.Button(app, text="Set Alarm", command=set_alarm)
set_alarm_button.pack()

alarm_time_label = tk.Label(app, text="Enter the alarm time (HH:MM):")
alarm_time_label.pack()

alarm_time_entry = tk.Entry(app)
alarm_time_entry.pack()

alarm_status_label = tk.Label(app, text="")
alarm_status_label.pack()

# Periodically update the displayed time 
app.after(1000, show_selected_time)

# Start the main event loop 
app.mainloop()

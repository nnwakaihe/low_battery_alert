import os
import ctypes
import winsound
import threading
from tkinter import Tk, Label, Button
from psutil import sensors_battery

def check_battery_and_notify():
    """Check the battery level and notify if it is at 15% and not charging."""
    battery = sensors_battery()
    print(battery.percent)
    if battery.percent <= 15 and not battery.power_plugged:
        show_alert("low_battery.wav", "Battery is at 15%! Please plug in your charger.")
    elif battery.power_plugged:
        show_alert("charging.wav", "Laptop is now charging.")

def play_audio(file):
    """Play the audio file in a loop."""
    while audio_playing[0]:
        winsound.PlaySound(file, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

def show_alert(audio_file, message):
    """Show a pop-up window alerting the user."""
    def close_window():
        """Stop audio and close the pop-up window."""
        audio_playing[0] = False
        winsound.PlaySound(None, winsound.SND_PURGE)
        root.destroy()

    root = Tk()
    root.title("Battery Alert")
    root.geometry("300x150")

    Label(root, text=message, wraplength=250, font=("Arial", 12)).pack(pady=20)
    Button(root, text="OK", command=close_window, font=("Arial", 10)).pack(pady=10)

    audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
    audio_thread.daemon = True
    audio_thread.start()

    root.mainloop()


# Paths to the audio files
low_battery_audio = "Low_Battery_Audio.wav"
charging_audio = "Charging_Audio.wav"

# Check if the audio files exist
for audio_file in [low_battery_audio, charging_audio]:
    if not os.path.exists(audio_file):
        ctypes.windll.user32.MessageBoxW(0, f"Audio file not found: {audio_file}", "Error", 0x10)
        exit()

# A flag to control the audio playback
audio_playing = [True]

# Periodically check the battery level
try:
    while True:
        check_battery_and_notify()
except KeyboardInterrupt:
    print("Exiting...")


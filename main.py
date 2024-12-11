import os
import ctypes
import winsound
import threading
from tkinter import Tk, Label, Button
from psutil import sensors_battery

def check_battery_and_notify():
    """Check the battery level and notify if it is at 15% and not charging."""
    battery = sensors_battery()
    if battery.percent <= 15 and not battery.power_plugged:
        show_alert()

def play_audio():
    """Play the audio file in a loop."""
    while audio_playing[0]:
        winsound.PlaySound(audio_file, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

def show_alert():
    """Show a pop-up window alerting the user of low battery."""
    def close_window():
        """Stop audio and close the pop-up window."""
        audio_playing[0] = False
        winsound.PlaySound(None, winsound.SND_PURGE)
        root.destroy()

    # Stop if the battery starts charging
    def monitor_battery():
        while root.winfo_exists():
            if sensors_battery().power_plugged:
                close_window()
                break

    root = Tk()
    root.title("Low Battery Alert")
    root.geometry("300x150")

    Label(root, text="Battery is at 15%! Please plug in your charger.", wraplength=250, font=("Arial", 12)).pack(pady=20)
    Button(root, text="OK", command=close_window, font=("Arial", 10)).pack(pady=10)

    audio_thread = threading.Thread(target=play_audio)
    audio_thread.daemon = True
    audio_thread.start()

    battery_monitor_thread = threading.Thread(target=monitor_battery)
    battery_monitor_thread.daemon = True
    battery_monitor_thread.start()

    root.mainloop()


def main():
    # Set the path to the audio file
    # Replace 'low_battery.wav' with the full path to your audio file
    audio_file = "low_battery.wav"

    # Check if the audio file exists
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


if __name__ == '__main__':
    main()
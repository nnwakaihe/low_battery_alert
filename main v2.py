import os
import ctypes
import winsound
import threading
from tkinter import Tk, Label, Button
from psutil import sensors_battery
import time

audio_playing = [True]  # Global flag to control audio playback

def check_battery_and_notify(low_battery_audio, charging_audio):
    """Check the battery level and notify if it is at 15% and not charging."""

    def close_window():
        """Stop audio and close the pop-up window."""
        winsound.PlaySound(None, winsound.SND_PURGE)  # Stop the current audio
        if root:
            root.destroy()  # Close the pop-up window

    battery = sensors_battery()
    print(f"Battery percentage: {battery.percent}%")

    # if battery.percent <= 15 and not battery.power_plugged:
    if 10 < 15:
        # Show low battery alert
        # print("low ass battery")
        root = Tk()
        root.title("Battery Alert")
        root.geometry("300x150")
        root.attributes('-topmost', True)

        Label(root, text="Battery is at 15%! Please plug in your charger.", wraplength=250, font=("Arial", 12)).pack(pady=20)
        Button(root, text="OK", command=close_window, font=("Arial", 10)).pack(pady=10)

        # Play the low battery audio once
        # threading.Thread(target=play_audio, args=(low_battery_audio,), daemon=True).start()

        # Periodically check for charging status inside the event loop
        def check_charging_status():
            new_battery = sensors_battery()
            if new_battery.power_plugged:  # If the battery is now plugged in
                close_window()  # Close the pop-up
                # play_audio(charging_audio)  # Play charging audio
            else:
                root.after(1000, check_charging_status)  # Re-check after 2 seconds

        check_charging_status()  # Start checking for charging status
        root.mainloop()


def play_audio(file):
    """Play the audio file once."""
    winsound.PlaySound(file, winsound.SND_FILENAME | winsound.SND_ASYNC)


def show_alert(audio_file, message):
    """Show a pop-up window alerting the user."""

    def close_window():
        """Stop audio and close the pop-up window."""
        winsound.PlaySound(None, winsound.SND_PURGE)
        root.destroy()

    root = Tk()
    root.title("Battery Alert")
    root.geometry("300x150")

    Label(root, text=message, wraplength=250, font=("Arial", 12)).pack(pady=20)
    Button(root, text="OK", command=close_window, font=("Arial", 10)).pack(pady=10)

    # Play audio once when the alert is shown
    threading.Thread(target=play_audio, args=(audio_file,), daemon=True).start()

    root.mainloop()


def main():
    # Paths to the audio files
    low_battery_audio = os.path.join(os.path.dirname(__file__), "Low_Battery_Audio.wav")
    charging_audio = os.path.join(os.path.dirname(__file__), "Charging_Audio.wav")

    # Check if the audio files exist
    for audio_file in [low_battery_audio, charging_audio]:
        if not os.path.exists(audio_file):
            ctypes.windll.user32.MessageBoxW(0, f"Audio file not found: {audio_file}", "Error", 0x10)
            exit()

    # Periodically check the battery level
    try:
        while True:
            check_battery_and_notify(low_battery_audio, charging_audio)
            time.sleep(30)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()

import os
import ctypes
import winsound
import threading
from tkinter import Tk, Label, Button
from psutil import sensors_battery
import time
#
# audio_playing = [True]  # Global flag to control audio playback






def main():

    def close_window():
        """Stop audio and close the pop-up window."""
        winsound.PlaySound(None, winsound.SND_PURGE)  # Stop the current audio
        if root:
            root.destroy()  # Close the pop-up window


    # Paths to the audio files
    low_battery_audio = os.path.join(os.path.dirname(__file__), "Low_Battery_Audio.wav")
    charging_audio = os.path.join(os.path.dirname(__file__), "Charging_Audio.wav")

    # Check if the audio files exist
    for audio_file in [low_battery_audio, charging_audio]:
        if not os.path.exists(audio_file):
            ctypes.windll.user32.MessageBoxW(0, f"Audio file not found: {audio_file}", "Error", 0x10)
            exit()

    first_alert = True
    # Periodically check the battery level
    try:
        while True:
            """Check the battery level and notify if it is at 15% and not charging."""
            battery = sensors_battery()
            print(f"Battery percentage: {battery.percent}%")

            # if battery.percent <= 15 and not battery.power_plugged:
            if 10 < 15 and first_alert:
                first_alert = False
                # Construct low battery Popup Window
                root = Tk()
                root.title("Battery Alert")
                root.geometry("300x150")
                root.attributes('-topmost', True)
                Label(root, text="Battery is at 15%! Please plug in your charger.", wraplength=250,
                      font=("Arial", 12)).pack(pady=20)
                Button(root, text="OK", command=close_window, font=("Arial", 10)).pack(pady=10)

                # Play the low battery audio once
                # threading.Thread(target=play_audio, args=(low_battery_audio,), daemon=True).start()

                root.mainloop() #initialize window
            time.sleep(30)

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
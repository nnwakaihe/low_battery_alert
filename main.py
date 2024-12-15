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
            # print(f"Battery percentage: {battery.percent}%")
            print(f"Battery percentage: {10}%")
            # if battery.percent <= 15 and not battery.power_plugged:
            if 10 < 15 and first_alert:
                print('battery is low af')
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
                def check_charging_status():
                    """Check if the battery starts charging, and close the window."""
                    new_battery = sensors_battery()
                    fake_battery = False
                    # if new_battery.power_plugged:  # If the battery is now charging
                    if fake_battery:  # If the battery is now charging
                        print('now charging, closing window')
                        close_window()
                        winsound.PlaySound(charging_audio, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    else:
                        root.after(20000, check_charging_status)  # Re-check after 2 seconds
                check_charging_status()  # Start checking charging status
                root.mainloop() #initialize window

            elif battery.power_plugged and root:
                print('the window should already be closed since were charging, but just in case CLOSE')
                close_window()  # Ensure the window is closed if charging
                first_alert = True

            time.sleep(30)

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
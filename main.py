import os
import ctypes
import winsound
import threading
from tkinter import Tk, Label, Button
from psutil import sensors_battery
import time

###Working loops
#Unplug, Plug, Unplug
#Plug, Unplug, Plug

def validating_audio():
    # Creating and validating audio file paths
    print('set audio file paths')
    low_battery_audio = os.path.join(os.path.dirname(__file__), "Low_Battery_Audio.wav")
    charging_audio = os.path.join(os.path.dirname(__file__), "Charging_Audio.wav")
    # Check if the audio files exist
    for audio_file in [low_battery_audio, charging_audio]:
        if not os.path.exists(audio_file):
            ctypes.windll.user32.MessageBoxW(0, f"Audio file not found: {audio_file}", "Error", 0x10)
            exit()
    return low_battery_audio, charging_audio


def close_window(root):
    """Stop audio and close the pop-up window."""
    winsound.PlaySound(None, winsound.SND_PURGE)  # Stop the current audio
    if window_open[0]:
        try:
            print('closing popup window')
            root.destroy()  # Close the pop-up window
            window_open[0] = False
            # root = None  # Ensure root is set to None after destruction
        except Exception as e:
                print(f"Error closing window: {e}")


def play_audio(file):
    """Play the audio file once."""
    if audio_playing[0]:
        print(f"playing {file}")
        winsound.PlaySound(file, winsound.SND_FILENAME | winsound.SND_ASYNC)


# "Global" variables, will use these for controlling things as we loop in and out of if statements
audio_playing = [False]  # Global flag to control audio playback
window_open = [False]


def main():
    low_battery_audio, charging_audio = validating_audio()

    first_alert = [True]
    # Periodically check the battery level
    try:
        while True:
            """Check the battery level and notify if it is at 15% and not charging."""
            battery = sensors_battery()
            # print(f"Battery percentage: {battery.percent}%")
            print(f"Top of while loop. Battery percentage: {10}%")

            # elif battery.percent <= 15 and not battery.power_plugged:
            if 10 < 15 and not battery.power_plugged:
                print('defining popup window attributes')
                first_alert = False

                # Construct low battery Popup Window
                root = Tk()
                root.title("Battery Alert")
                root.geometry("300x150")
                root.attributes('-topmost', True)
                Label(root, text="Battery is at 15%! Please plug in your charger.", wraplength=250,
                      font=("Arial", 12)).pack(pady=20)
                Button(root, text="OK", command=close_window(root), font=("Arial", 10)).pack(pady=10)

                # Play the low battery audio once
                if not battery.power_plugged:
                    print('playing dying audio')
                    audio_playing[0] = True
                    threading.Thread(target=play_audio, args=(low_battery_audio,), daemon=True).start()
                    print('displaying popup')
                def check_charging_status():
                    """Check if the battery starts charging, and close the window."""
                    print('checking charge status')
                    new_battery = sensors_battery()
                    fake_battery = False
                    if new_battery.power_plugged:  # If the battery is now charging
                    # if fake_battery:  # If the battery is now charging
                        print('now charging, closing window if open')
                        close_window(root)
                        play_audio(charging_audio)
                        audio_playing[0] = False
                    else:
                        print('still not charging, will check again later')
                        root.after(2000, check_charging_status)  # Re-check after 2 seconds
                check_charging_status()  # Start checking charging status
                print('\n')
                window_open[0] = True
                root.mainloop() #initialize window

            elif battery.power_plugged:
                print('charging RN')
                if window_open[0]:
                    print('just started charing, closing popup')
                    close_window(root)  # Ensure the window is closed if charging
                first_alert = [True]
                print('\n')

            time.sleep(5)

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
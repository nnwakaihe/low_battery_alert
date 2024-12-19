import os
import ctypes
import winsound
import threading
from tkinter import Tk, Label, Button
from psutil import sensors_battery
import time

# "Global" variables, will use these for controlling things as we loop in and out of if statements
audio_playing = [False]
window_open = [False]
closed_manually = [False]


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


def manual_close(root):
    close_window(root)
    closed_manually[0] = True
    print('popup closed manually')


def play_audio(file):
    """Play the audio file once."""
    if audio_playing[0]:
        print(f"playing {file}")
        winsound.PlaySound(file, winsound.SND_FILENAME | winsound.SND_ASYNC)


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


def main():
    low_battery_audio, charging_audio = validating_audio()

    # Periodically check the battery level
    try:
        while True:
            """Check the battery level and notify if it is at 15% and not charging."""
            battery = sensors_battery()
            print(f"Battery percentage: {battery.percent}%")
            # If the battery is low, and the battery isn't plugged in, and the popup wasn't closed manually
            if (battery.percent <= 50 or battery.percent <= 15) and not battery.power_plugged and not closed_manually[0]:
                # Construct low battery Popup Window
                print('defining popup window attributes')
                root = Tk()
                root.title("Battery Alert")
                root.geometry("300x150")
                root.attributes('-topmost', True)
                Label(root, text="Battery is Low! Please plug in your charger.", wraplength=250,
                      font=("Arial", 12)).pack(pady=20)
                Button(root, text="OK", command=lambda: manual_close(root), font=("Arial", 10)).pack(pady=10)

                # Play the low battery audio once
                print('playing dying audio')
                audio_playing[0] = True
                threading.Thread(target=play_audio, args=(low_battery_audio,), daemon=True).start()

                def check_charging_status():
                    """Check if the battery starts charging, and close the window."""
                    print('checking charge status')
                    new_battery = sensors_battery()
                    fake_battery = False
                    if new_battery.power_plugged:  # If the battery is now charging
                        print('now charging, closing window if open')
                        close_window(root)
                        play_audio(charging_audio)
                        audio_playing[0] = False
                    else:
                        print('still not charging, will check again later')
                        root.after(2000, check_charging_status)  # Re-check after 2 seconds
                check_charging_status()  # Start checking charging status
                window_open[0] = True
                print('displaying popup')
                root.mainloop() #initialize window

            elif battery.power_plugged:
                print('charging RN')
                if window_open[0]:
                    print('just started charing, closing popup')
                    close_window(root)  # Ensure the window is closed if charging
                closed_manually[0] = False

            time.sleep(5)
            print('\n')

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()

    # pyinstaller --name Low_Battery_Notification --onefile --noconsole --add-data "Low_Battery_Audio.wav;." --add-data "Charging_Audio.wav;." main.py
# Battery Alert

This repository contains a Python script designed to alert users when their laptop's battery reaches a critical low level. Frustrated with my laptop's battery dying without warning, I created this script to solve the problem. When the battery drops to 15%, a pop-up window appears, and a snippet from the show *Futurama* plays, where a robot freaks out due to a low power supply. When the laptop is plugged in to charge, the robot's voice calms down, providing a fun and effective way to monitor battery levels.

This guide provides instructions to:
1. Convert your Python script into an executable file (`.exe`).
2. Schedule the `.exe` file to run automatically using Task Scheduler.

---

## **Step 1: Converting the Python Script into an Executable File**

### **Requirements**
- Install Python and ensure it is added to your system PATH.
- Install `pyinstaller` to convert the Python script into an executable.
  ```bash
  pip install pyinstaller
  ```

### **Steps**
1. Open a command prompt and navigate to the directory containing your Python script (`main.py`).
   ```bash
   cd path\to\your\script
   ```

2. Run the `pyinstaller` command to create the executable, including the necessary audio files:
   ```bash
   pyinstaller --name Low_Battery_Notification --onefile --noconsole --add-data "Low_Battery_Audio.wav;." --add-data "Charging_Audio.wav;." main.py
   ```
   - `--onefile`: Packages the script into a single `.exe` file.
   - `--add-data`: Ensures the required audio files are bundled with the `.exe`.
     - For Windows, separate paths and destinations with a semicolon (`;`).

3. After the command completes, the `.exe` file will be located in the `dist` directory:
   ```
   dist\Low_Battery_Notification.exe
   ```

4. Test the `.exe` by running it directly to ensure the script behaves as expected.

---

## **Step 2: Scheduling the Executable with Task Scheduler**

### **Steps**
1. Open **Task Scheduler** (search for it in the Start menu).

2. Click **Create Task** on the right panel.

3. In the **General** tab:
   - Provide a name for the task (e.g., `Battery Alert`).
   - Select **Run only when the user is logged on**.
   - Check **Run with highest privileges**.

4. Go to the **Triggers** tab:
   - Click New > Set "Begin the task" to At log on.
   - Click **OK**.

5. Go to the **Actions** tab:
   - Click **New** to create a new action.
   - Set the **Action** to **Start a program**.
   - In the **Program/script** field, browse to select the `.exe` file (e.g., `dist\Low_Battery_Notification.exe`).
   - **Important**: In the **Start in (optional)** field, add the folder path where the `.exe` is located (e.g., `C:\path\to\dist`).
   - Click **OK**.

6. Go to the **Conditions** tab:
   - Uncheck **Start the task only if the computer is on AC power**.
   - Adjust other conditions as needed.

7. Click **OK** to save the task.

8. Test the task by right-clicking it in Task Scheduler and selecting **Run**.

---

## **Notes**
- Ensure the `.exe` file and audio files are in the same directory when testing and running the task.
- Use the **History** tab in Task Scheduler to debug issues with the scheduled task.
- Modify the script or Task Scheduler settings as necessary for your specific use case.

---

This setup ensures the battery alert runs automatically and efficiently at system startup or other configured intervals.


source myenv/bin/activate
pip install firebase_admin
python3 camera_firebase.py

install packages into myenv
/home/gwenzhang/Documents/Robin/myenv/bin/python -m pip install paho-mqtt

find ip address:
hostname -I

change network:
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf


use the ps command or the htop utility to check for running processes

Using ps:
Open a terminal window and run the following command:
ps aux | grep -i camera
This command will display a list of processes containing the word "camera". Look for any processes related to the camera that might be using it.

Using htop:
If you have htop installed (if not, you can install it using sudo apt install htop), you can run it in the terminal by simply typing:
htop
This will open an interactive process viewer. You can navigate through the list of processes using the arrow keys and look for any processes related to the camera.

Once you identify any processes that might be using the camera, you can try stopping or killing them to free up the camera resource for your script. Use the kill command followed by the process ID (PID) to terminate a process. For example:

bash
Copy code
sudo kill PID
Replace PID with the actual process ID of the process you want to terminate.


# To achieve your goals of running the script automatically on Raspberry Pi boot and connecting to WiFi automatically, you can follow these steps:

Auto-start the script on boot:

You can use systemd to automatically start your Python script on boot. Create a systemd service unit file for your script.
Here's an example of how to create a systemd service unit file:
bash
Copy code
sudo nano /etc/systemd/system/my_script.service
Add the following content to the file:
makefile
Copy code
[Unit]
Description=My Script Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /path/to/your/script.py

[Install]
WantedBy=multi-user.target
Replace /path/to/your/script.py with the actual path to your Python script.
Save the file and exit the editor.
Enable the service to start on boot:
bash
Copy code
sudo systemctl enable my_script.service
Reboot your Raspberry Pi to apply the changes:
bash
Copy code
sudo reboot
Connect to WiFi automatically:

You can configure your Raspberry Pi to connect to a WiFi network automatically by setting up the network configuration file.
Open the network configuration file for editing:
bash
Copy code
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
Add the following lines to the end of the file:
makefile
Copy code
network={
    ssid="YourNetworkSSID"
    psk="YourNetworkPassword"
}
Replace YourNetworkSSID and YourNetworkPassword with your WiFi network SSID and password, respectively.
Save the file and exit the editor.
Reboot your Raspberry Pi:
bash
Copy code
sudo reboot
With these steps, your Raspberry Pi should automatically connect to WiFi on boot and start running your Python script as soon as it boots up. Make sure to replace /path/to/your/script.py with the actual path to your Python script, and YourNetworkSSID and YourNetworkPassword with your WiFi network credentials.






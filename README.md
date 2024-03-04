source myenv/bin/activate
pip install firebase_admin
python3 camera_firebase.py

# install packages into myenv
/home/gwenzhang/Documents/Robin/myenv/bin/python -m pip install paho-mqtt

# find ip address:
hostname -I



# use the ps command or the htop utility to check for running processes
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


# Connect to WiFi automatically:
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
network={
    ssid="YourNetworkSSID"
    psk="YourNetworkPassword"
}


# create new service file
make new service file
sudo nano /etc/systemd/system/YourNewServiceName.service
template
[Unit]
Description=My Script Service
After=multi-user.target network-online.target
Wants=network-online.target

[Service]
Type=idle
User=gwenzhang
Group=gwenzhang
WorkingDirectory=/home/pi/my_script_directory
ExecStart=/usr/bin/python3 /home/pi/my_script_directory/my_script.py
Restart=on-failure

[Install]
WantedBy=multi-user.target

reload and enable the service
sudo systemctl daemon-reload
sudo systemctl enable myscript.service
sudo systemctl start myscript.service

check status
sudo systemctl status YourNewServiceName.service








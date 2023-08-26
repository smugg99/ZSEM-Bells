
<pre>
  _________  _____ __  __       ____       _ _     
 |__  / ___|| ____|  \/  |     | __ )  ___| | |___ 
   / /\___ \|  _| | |\/| |_____|  _ \ / _ \ | / __|
  / /_ ___) | |___| |  | |_____| |_) |  __/ | \__ \
 /____|____/|_____|_|  |_|     |____/ \___|_|_|___/
</pre>

A program that manages bells in my school...

<div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center;">
    <img src="https://i.imgur.com/CDXbbhS.jpg" alt="image" width="256" height="256" style="margin: 10px;">
    <img src="https://i.imgur.com/X4R9076.jpg" alt="image" width="256" height="256" style="margin: 10px;">
    <img src="https://i.imgur.com/FmvJAQ8.jpg" alt="image" width="256" height="256" style="margin: 10px;">
</div>

# Prerequisites (tested on) 📚
- Python >3.10.6
- Pip >22.0.2
- Git >2.34.1

# Setup ⚙️

## Automatic installation
0. 
```shell
chmod a+x ./install.sh
```

1. Run the script

## Manual installation
0. Install venv  and python3 header files (if needed):
```shell
sudo apt install python3 python3-venv
```
```shell
sudo apt install python3-venv
```
```shell
sudo apt install python3-dev
```
1. Clone this repo:
```shell
git clone https://github.com/SmeggMann99/ZSEM-Bells.git/
```
2. Cd into the directory:
```shell
cd ./ZSEM-Bells
```
3. Clone my fork of the OPI.GPIO:
```shell
git clone https://github.com/SmeggMann99/OPI.GPIO.git/
```
3. Setup the virtual environment:
```shell
python3 -m venv venv
```
```shell
source ./venv/bin/activate
```
5. Build the OPI.GPIO module:
```shell
cd OPI.GPIO
```
```shell
sudo python3 setup.py install
```
```shell
pip install ./
```
6. Install required packages
```shell
pip install -r requirements.txt
```
7. Make the main file executable 
```shell
chmod a+x ./main.py
```

# Running ⚡
### Option A:
1. Run the main script directly
```shell
./main.py &
```
### Option B (WIP):
1. Make a system service/wizard 🧙🏻‍♂️


### Information ℹ️
Instructions for further maintainers are currently still being work on, but if you need help or you have any questions about this piece of software, message me on Discord (link is on my profile) or reach to me directly.
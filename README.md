<pre align="center">
  _________  _____ __  __       ____       _ _     
 |__  / ___|| ____|  \/  |     | __ )  ___| | |___ 
   / /\___ \|  _| | |\/| |_____|  _ \ / _ \ | / __|
  / /_ ___) | |___| |  | |_____| |_) |  __/ | \__ \
 /____|____/|_____|_|  |_|     |____/ \___|_|_|___/
</pre>

<h5 align="right"> A program that manages bells in my school...</h1>

<br>
<h1 align="center">Prerequisites (tested on) 📚</h1>

- Python >3.10.6
- Pip >22.0.2
- Git >2.34.1

<br>
<h1 align="center">Setup ⚙️</h1>

<br>
<h2 align="center">Automatic</h2>

0. Make the installer script executable

```shell
chmod a+x ./install.sh
```

1. Run the script, wait till the installation completes

<br>
<h2 align="center">Manual</h2>
<h5 align="right">(if something breaks, or you're not lazy)</h4>

0. Install venv and python3 header files (if needed):

```shell
sudo apt install python3 python3-venv
```

```shell
sudo apt install python3-venv
```

```shell
sudo apt install python3-dev
```

<br>
1. Clone this repo:

```shell
git clone https://github.com/DudusJestem/ZSEM-Bells.git/
```

<br>
2. Cd into the directory:

```shell
cd ./ZSEM-Bells
```

<br>
3. Clone my fork of the OPI.GPIO:

```shell
git clone https://github.com/DudusJestem/OPI.GPIO.git/
```

<br>
4. Setup the virtual environment:

```shell
python3 -m venv venv
```

```shell
source ./venv/bin/activate
```

<br>
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

<br>
6. Install required packages

```shell
pip install -r requirements.txt
```

<br>
7. Make the main file executable

```shell
chmod a+x ./main.py
```

<br>
<h1 align="center">Running ⚡</h2>

<br>
<h2 align="center">Option A</h2>

1. Run the main script directly

```shell
./main.py &
```

<br>
<h2 align="center">Option B (WIP)</h2>

1. Use the runner script 🧙🏻‍♂️
<br>

<h2 align="center">Option A (recommended)</h2>

1. Use systemctl
2. Create a service file using the template file in the repository root directory
3. Place the service file in "/etc/systemd/system" or in other system service directory
4. Enable and start the service:
```shell
systemctl enable zsem_bells
```
```shell
systemctl start zsem_bells
```

<br>

<h1 align="center">Information ℹ️</h1>

Instructions for further maintainers are currently still being work on, but if you need help or you have any questions about this piece of software, message me on Discord (link is on my profile) or reach to me directly.

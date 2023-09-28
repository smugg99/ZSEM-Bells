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

0. Make the installer script executable

```shell
chmod a+x ./install.sh
```

1. Run the script, wait till the installation completes


<br>
<h1 align="center">Running ⚡</h2>


<br>
<h2 align="center">Use systemctl (recommended)</h2>

1. Create and fill in the service file using the template file

2. Place the service file in "/etc/systemd/system" or in other system services directory

3. Enable and start the service:

```shell
systemctl enable zsem_bells
```
```shell
systemctl start zsem_bells
```

<br>
<h2 align="center">Run the main script (use for testing only)</h2>

```shell
./main.py &
```

<br>
<h2 align="center">Use the almost ready runner script 🧙🏻‍♂️</h2>

1. I ain't getting paid 🗿


<br>
<h1 align="center">Information ℹ️</h1>

Instructions for further maintainers are currently still being work on, but if you need help or you have any questions about this piece of software, message me on Discord (link is on my profile) or reach to me directly.

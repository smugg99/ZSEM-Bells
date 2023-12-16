#!/bin/bash

opirepo=https://github.com/smugg99/OPI.GPIO.git/

# Function to install a package if it's not already installed
install_if_not_installed() {
    PACKAGE=$1
    if ! dpkg -l | grep -q $PACKAGE; then
        echo "$PACKAGE is not installed. Installing..."
        sudo apt install -y $PACKAGE
    else
        echo "$PACKAGE is already installed"
    fi
}

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install required packages
install_if_not_installed python3
install_if_not_installed python3-pip

install_if_not_installed python3-venv
install_if_not_installed python3-dev
install_if_not_installed python3-dialog
install_if_not_installed python3-systemd

install_if_not_installed git


# Check if systemctl is installed, and if not, install it,
# it's usually installed because it's used internally by this system
if ! command -v systemctl &>/dev/null; then
    install_if_not_installed systemd
fi

# Create and activate virtual environment
echo "Creating and activating virtual environment"
python3 -m venv venv
source ./venv/bin/activate

# Check and install OPI.GPIO
if python3 -c "import OPI.GPIO" &>/dev/null; then
    echo "OPI.GPIO is already installed"
else
    echo "OPI.GPIO is not installed. Cloning..."
    git clone $opirepo
    
    echo "Installing OPI.GPIO module"
    pushd OPI.GPIO
    python3 setup.py install
    pip3 install ./
    popd
fi

# Install dependencies from requirements.txt
echo "Installing dependencies"
./venv/bin/pip install -r requirements.txt

# Deactivate virtual environment
echo "Deactivating virtual environment"
deactivate


# Automatically retrieve the current username and primary group
username=$USER
group=$(id -gn $USER)
config_file="service_config.txt"

service_filename="zsem_bells.service"
service_file_path="/etc/systemd/system"
service_description="ZSEM-Bells drivers system service"

while true; do
    # If config file exists, load values from it
    if [ -f "$config_file" ]; then
        source "$config_file"
    fi

    # Display currently set values
    echo "Current username: $username"
    echo "Current group: $group"

    read -p "Enter working directory: " new_working_directory
    working_directory=${new_working_directory:-$working_directory}

    read -p "Enter virtual environment path: " new_venv_path
    venv_path=${new_venv_path:-$venv_path}

    read -p "Enter main script path: " new_script_path
    script_path=${new_script_path:-$script_path}

    # Save the new values to the config file
    cat << EOF > "$config_file"

working_directory="$working_directory"
venv_path="$venv_path"
script_path="$script_path"
service_filename="$service_filename"
service_file_path="$service_file_path"

EOF

    # Confirm user actions
    read -p "Confirm to create '$service_filename' with provided settings? (yes/no): " confirm

    if [ "$confirm" == "yes" ]; then
        # Create the service file
        cat << EOF > zsem_bells.service
[Unit]
Description=$service_description
After=network.target

[Service]
User=$username
Group=$group
WorkingDirectory=$working_directory
Environment="PATH=$venv_path/bin"
ExecStart=$venv_path/bin/python3 $script_path
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=zsem_bells

[Install]
WantedBy=multi-user.target
EOF

        echo "Service file '$service_filename' created"
        break  # Exit the loop if user confirms
    else
        echo "Operation cancelled. Going through configuration again"
    fi
done

# Move the service file to the common system service directory
echo "Moving service file to $service_file_path"
if [ -f "$service_filename" ]; then
    sudo mv zsem_bells.service $service_file_path
    echo "Service file '$service_filename' moved to $service_file_path"
else
    echo "Service file '$service_filename' somehow not found. Skipping move."
fi

echo "Deactivating virtual environment"
deactivate

echo "All packages checked and installed if needed"
echo "Installation completed!"

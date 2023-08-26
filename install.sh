#!/bin/bash

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

# Install python3 if not installed
install_if_not_installed python3

# Install python3-pip if not installed
install_if_not_installed python3-pip

# Install other required packages
install_if_not_installed python3-venv
install_if_not_installed python3-dev
install_if_not_installed git

# Create and activate virtual environment
echo "Creating and activating virtual environment"
python3 -m venv venv
source ./venv/bin/activate

# Check and install OPI.GPIO
if python3 -c "import OPI.GPIO" &>/dev/null; then
    echo "OPI.GPIO is already installed"
else
    echo "OPI.GPIO is not installed. Cloning..."
    git clone https://github.com/SmeggMann99/OPI.GPIO.git/
    
    echo "Installing OPI.GPIO module"
    pushd OPI.GPIO
    sudo python3 setup.py install
    pip install ./
    popd
fi

# Install dependencies from requirements.txt
echo "Installing dependencies"
pip install -r requirements.txt

echo "All packages checked and installed if needed"
echo "Installation completed!"

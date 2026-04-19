How to install:

Install tkinter
``` bash
sudo apt install python3-tk
```

Create and activate python virtual environment
```bash
virtualenv .venv
source .venv/bin/activate
```

Install python packages
```bash
pip3 install -r requirements.txt
```

Set permissions for /dev/i2c

```bash
# If group does not exist
sudo groupadd i2c   

sudo usermod -aG i2c $USER

# Create udev rule
sudo nano /etc/udev/rules.d/99-i2c.rules

KERNEL=="i2c-[0-9]*", GROUP="i2c", MODE="0660"

# Reload rules
sudo udevadm control --reload-rules
sudo udevadm trigger

``` 

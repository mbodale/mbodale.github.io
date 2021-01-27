# welcome-home
Welcome home light automation with UniFi AC and lightwaverf

Simple script dedicated to specific setup Ubiquiti Networks UniFi access point + lightwaverf bridge


# What does it do?

The script compares curent time with today's sunrise and sunset times. If it's 30 min before sunset or sunrise and script will detect your device, for example mobile phone logging in to wifi AC, it will send a signal to lightwaverf bridge to switch on or off specific device.

# Running 

- Please update hello-home.py
```
home.lat = '51:28:38'
```
To match your location. This wil quarantee corect sunrise/sunset times

- Instal requirements
```sh
$ pip install -r requirements.txt
```

- Run script -h to display menu
```sh
$ ./hello-home.py -h
usage: hello-home.py [-h] [-c CONTROLLER] [-u USERNAME] [-p PASSWORD]
                     [-b CPORT] [-v VERSION] [-s SITEID] [-l LIGHTWAVERF]
                     [-t LPORT] [-a ACTIVATE] [-m MAC]

optional arguments:
  -h, --help            show this help message and exit
  -c CONTROLLER, --controller CONTROLLER
                        the controller address (default "unifi")
  -u USERNAME, --username USERNAME
                        the controller username (default("admin")
  -p PASSWORD, --password PASSWORD
                        the controller password
  -b CPORT, --cport CPORT
                        the controller port (default "8443")
  -v VERSION, --version VERSION
                        the controller base version (default "v5")
  -s SITEID, --siteid SITEID
                        the site ID, UniFi >=3.x only (default "default")
  -l LIGHTWAVERF, --lightwaverf LIGHTWAVERF
                        Lightwaverf bridge IP
  -t LPORT, --lport LPORT
                        Lightwaverf bridge port (default 2011)
  -a ACTIVATE, --activate ACTIVATE
                        Activate device example (Room1 Device1 ON = R1D1F1
  -m MAC, --mac MAC     Mac address of the device to monitor
$ 
```
An example of swithing on the light in Room1 Device1 ON

```
$ ./hello-home.py -c <UniFi IP> -u <username> -p <password> -l <LWRFbridgeIP> -a R1D1F1

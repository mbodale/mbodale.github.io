#!/usr/bin/env python3

import argparse
import datetime
import socket
import time

import ephem
import requests
from dateutil import parser

parser_arg = argparse.ArgumentParser()
parser_arg.add_argument('-c', '--controller', default='unifi', help='the controller address (default "unifi")')
parser_arg.add_argument('-u', '--username', default='admin', help='the controller username (default("admin")')
parser_arg.add_argument('-p', '--password', default='password', help='the controller password')
parser_arg.add_argument('-b', '--cport', default='8443', help='the controller port (default "8443")')
parser_arg.add_argument('-v', '--version', default='v5', help='the controller base version (default "v5")')
parser_arg.add_argument('-s', '--siteid', default='default', help='the site ID, UniFi >=3.x only (default "default")')
parser_arg.add_argument('-l', '--lightwaverf', help='Lightwaverf bridge IP')
parser_arg.add_argument('-t', '--lport', default='2011', help='Lightwaverf bridge port (default 2011)')
parser_arg.add_argument('-a', '--activate', default='R1D1F1', help='Activate device example (Room1 Device1 ON = R1D1F1')
parser_arg.add_argument('-m', '--mac', help='Mac address of the device to monitor')
args = parser_arg.parse_args()

sun = ephem.Sun()
home = ephem.Observer()
home.lat = '51:28:38'

'''
Disabling  warnings about insecure cert check being disable
'''
requests.packages.urllib3.disable_warnings()

session = requests.session()

mac_to_monitor = args.mac
controller_IP = args.controller
controller_port = args.cport
lightwaverf_IP = args.lightwaverf
lightwaverf_port = int(args.lport)
activate = args.activate

login_payload = '{"username":"' + args.username + '","password":"' + args.password + '","remember":true,"strict":true}'
login_url = 'https://{0}:{1}/api/login'.format(controller_IP, controller_port)
stats_conf_url = 'https://{0}:{1}/api/s/default/stat/sta'.format(controller_IP, controller_port)

login = session.post(login_url, login_payload, verify=False)

max_uptime = datetime.timedelta(seconds=60)


def convert_epoch(epoch):
	hdata = datetime.datetime.fromtimestamp(epoch)
	return hdata


while True:
	try:
		today = datetime.date.today()
		home.date = today
		sun_rise = parser.parse(str(home.next_rising(sun))) + datetime.timedelta(minutes=30)
		sun_set = parser.parse(str(home.next_setting(sun))) - datetime.timedelta(minutes=30)
		now = datetime.datetime.utcnow()
		print('Now: {3} | Today {0} sun will rise at {1} and set at {2}'.format(today, sun_rise, sun_set, now))

		if sun_rise > now or now > sun_set:
			refresh = 20
			all_stats = session.get(stats_conf_url).json()
			stats = dict((key, value) for key, value in all_stats.items() if key == 'data')
			for device_status in stats['data']:
				if device_status['mac'] == mac_to_monitor:
					uptime = datetime.timedelta(seconds=device_status['_uptime_by_uap'])
					print('Mac: {0} | Uptime; {1}'.format(device_status['mac'], uptime))
					if uptime < max_uptime:
						sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
						MESSAGE = str.encode("25769006,!{0}|Hi Damian|Welcome home!!".format(activate))
						sock.sendto(MESSAGE, (lightwaverf_IP, lightwaverf_port))
						sock.close()
						print('Lights on!')
						'''
						Since we use UDP which is proof to be not fault tolerant,
						we are resending same signal few times to make sure
						it will reach the lightwaverf bridge.
						Since this is always the same command, it doesnt revert change
						if previous command worked.
						'''
						refresh = 10
		else:
			print("It's day, no light needed")
			refresh = 60
		time.sleep(refresh)
	except (KeyboardInterrupt, SystemExit):
		print('Exiting ...')
		exit()
	except:
		print('We have encourage some problem')
		raise

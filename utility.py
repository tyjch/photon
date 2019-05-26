from scapy.all import *
from datetime import datetime
from playsound import playsound
import os

def get_hexdump_str(packet):
    dump = linehexdump(packet, dump=True)
    dump = dump.split(sep='  ')
    return dump[0], dump[1]

def convert_to_ts(iso_string):
	'''
	Adds trailing zeros to rounded fraction of iso8061 datetime, then create a timestamp from the formatted string
	'''

	ts, fraction = iso_string.rsplit('.', maxsplit=1)
	len_fraction = len(fraction)

	if len_fraction < 6:
		trailing_zeroes = '0' * (6-len_fraction)
		iso_string = ts + '.' + fraction + trailing_zeroes

	dt = datetime.fromisoformat(iso_string)
	ts = datetime.timestamp(dt)

	return ts

def alert(s='Alert'):
	os.system(f'say "{s}"')


if __name__ == '__main__':
    alert()

    iso = '3018-09-24T22:31:05.57745'
    ts = convert_to_ts(iso)
    print(ts)


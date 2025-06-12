import argparse
import re
import socket

from concurrent.futures import ThreadPoolExecutor


def cli():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--host', '-h', required=True, help='The Target IPv4 Address')
    parser.add_argument('--ports', '-p', required=True, help='Ports to Scan (Supported Formats: single port, start-end, comma-sep)')

    args = parser.parse_args()

    host: str = args.host
    ports: list[int] = parse_ports(args.ports) 

    print('Testing {}:'.format(host)) 

    # Sequential
    for port in ports:
        if is_open(host, port):
            print('{}: Open'.format(port))
        else:
            print('{}: Closed'.format(port))


    # Concurrent Scan
    


def is_open(host: str, port: int) -> bool:
	addr = (host, port)
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.settimeout(1)

		try:
			sock.connect(addr)
			return True
		except:
			return False


def parse_ports(ports: str) -> list[int]:
    re_dash = re.compile(r'^\d+-\d+$')
    re_csv = re.compile(r'^\d+(,\d+)*$')
    re_single = re.compile(r'^\d+$')

    if re_single.fullmatch(ports):
        return [int(ports)]

    if re_csv.fullmatch(ports):
        return list(map(int, ports.split(',')))

    if re_dash.fullmatch(ports):
        start = int(ports.split('-')[0])
        end = int(ports.split('-')[1])

        return list(range(start, end+1))

    raise ValueError('Error: ports {} is not in a valid format'.format(ports))


if __name__ == '__main__':
    cli()

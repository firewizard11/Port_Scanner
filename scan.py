import argparse
import socket


def cli():
	pass


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
	pass


if __name__ == '__main__':
	print('Starting Test...')
	
	test_host = 'scanme.nmap.org'
	test_ports = [22, 80, 443, 1024, 2000, 3000]

	print('Testing {}'.format(test_host))

	for port in test_ports:
		print('{}: {}'.format(port, is_open(test_host, port)))

	print('Test Complete!')

import argparse
import socket


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument('--target', '-t')
    parser.add_argument('--ports', '-p')

    args = parser.parse_args()

    target = args.target
    ports = args.ports

    print('Testing {}:'.format(target))
    if is_open(target, int(ports)):
        print('{}: Open'.format(ports))
    else:
        print('{}: Closed'.format(ports))


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
    cli()

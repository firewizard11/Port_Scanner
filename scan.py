import argparse
import socket


def cli():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--host', '-h', required=True, help='The Target IPv4 Address')
    parser.add_argument('--ports', '-p', required=True, help='Ports to Scan (Supported Formats: single port, start-end, comma-sep)')

    args = parser.parse_args()

    target:str = args.host
    ports: list[int] = args.ports

    # Single Port

    # Sequential Scan

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
	pass


if __name__ == '__main__':
    cli()

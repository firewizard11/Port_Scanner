import argparse
import re
import socket

from concurrent.futures import ThreadPoolExecutor


def cli():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--host', '-h', required=True, help='The Target IPv4 Address')
    parser.add_argument('--ports', '-p', required=True, help='Ports to Scan (Supported Formats: single port, start-end, comma-sep)')
    parser.add_argument('--threads', '-t',type=int, help='Max number of scans to perform at once')
    parser.add_argument('--verbose', '-v', action='store_true', help='Setting this will display closed ports')

    args = parser.parse_args()

    host: str = args.host

    if not validate_ip(host):
        print('Error: {} is not a valid IP'.format(host))
        return

    try:
        ports: list[int] = parse_ports(args.ports) 
    except ValueError as e:
        print(e)
        return

    for port in ports:
        if not validate_port(port):
            print('Error: {} is not a valid port'.format(port))
            return

    threads = args.threads 
    if threads and threads < 1:
        print('Error: --threads should be greater than 0, not {}'.format(threads))
        return

    verbose = args.verbose

    print('Testing {}:'.format(host)) 
    pool = None
    
    try:
        if not threads:
            # Sequential
            for port in ports:
                test_port(host, port, verbose)
        else:
            # Concurrent Scan
            pool = ThreadPoolExecutor(max_workers=threads)
        
            for port in ports:
                pool.submit(test_port, host, port, verbose)

            pool.shutdown()
    except KeyboardInterrupt:
        if pool:
            pool.shutdown(wait=False, cancel_futures=True)


def test_port(host: str, port: int, verbose: bool = False) -> None:
    if is_open(host, port):
        print('{}: Open'.format(port))
    elif verbose:
        print('{}: Closed'.format(port))


def is_open(host: str, port: int) -> bool:
	addr = (host, port)
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.settimeout(1)

		try:
			sock.connect(addr)
			return True
		except (TimeoutError, ConnectionRefusedError):
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

    raise ValueError('Error: ports {} is not in a valid format (e.g. number, start-end, number,number,...,number)'.format(ports))


def validate_port(port: int) -> bool:
    return 0 <= port <= 65535


def validate_ip(ip: str) -> bool:
    re_ip = re.compile(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$')
    
    if re_ip.fullmatch(ip):
        for octet in ip.split('.'):
            if not (0 <= int(octet) <= 255):
                return False
        return True
    else:
        return False


if __name__ == '__main__':
    cli()

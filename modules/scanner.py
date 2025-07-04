import socket

from concurrent.futures import ThreadPoolExecutor


def sequential_scan(host: str, ports: list[int], verbose: bool) -> set[int]:
    open_ports = set()
    for port in ports:
        test_port(host, port, verbose)
        open_ports.add(port)

    return open_ports


def concurrent_scan(
    host: str, ports: list[int], threads: int, verbose: bool
) -> set[int]:
    pool = ThreadPoolExecutor(max_workers=threads)
    open_ports = set()

    for port in ports:
        result = pool.submit(test_port, host, port, verbose).result()
        if result:
            open_ports.add(port)

    pool.shutdown()
    return open_ports


def test_port(host: str, port: int, verbose: bool = False) -> bool:
    if is_open(host, port):
        print("{}: Open".format(port))
        return True
    elif verbose:
        print("{}: Closed".format(port))
        return False


def is_open(host: str, port: int) -> bool:
    addr = (host, port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)

        try:
            sock.connect(addr)
            return True
        except (TimeoutError, ConnectionRefusedError):
            return False

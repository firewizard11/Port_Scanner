# Port Scanner

## Description

This is my own personal port scanner that I'm going to add to as I used it

## How to Use

Scan all ports on host '192.168.1.1' sequentially

`python3 scan.py -h 192.168.1.1 -p 1-65535` 

Scan Ports: 22,80,43,135,4444 on Host 127.0.0.1 with 40 ports at a time

`python3 scan.py -h 127.0.0.1 -p 22,80,43,135,4444 -t 40`


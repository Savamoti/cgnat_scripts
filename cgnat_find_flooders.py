#!/usr/bin/env python3

"""
cgnat_find_flooders.py


The script finds TCP and UDP flooders from CGNAT service.


Requirements:
* python3.6 >=
* python3.6 -m pip install tabulate


You can run it, like this:
```
# cgnat_find_flooders

TOP-10 port flooders by TCP
+----------------+-------------------+-------------------+-----------------+
| Private IP     |   TCP Utilization |   UDP Utilization | Public IP       |
|----------------+-------------------+-------------------+-----------------|
| 172.29.131.232 |              2000 |                 1 | x.x.x.x         |
| 172.29.158.103 |              2000 |               135 | x.x.x.x         |
| 172.29.131.27  |              2000 |                 4 | x.x.x.x         |
| 172.29.144.72  |              1999 |                 5 | x.x.x.x         |
| 172.29.142.56  |              1999 |                 4 | x.x.x.x         |
| 172.29.68.48   |              1999 |                16 | x.x.x.x         |
| 172.29.129.168 |              1997 |                20 | x.x.x.x         |
| 172.29.145.199 |              1996 |                23 | x.x.x.x         |
| 172.29.142.59  |              1950 |                41 | x.x.x.x         |
| 172.29.162.57  |              1914 |                 0 | x.x.x.x         |
+----------------+-------------------+-------------------+-----------------+

TOP-10 port flooders by UDP
+----------------+-------------------+-------------------+-----------------+
| Private IP     |   TCP Utilization |   UDP Utilization | Public IP       |
|----------------+-------------------+-------------------+-----------------|
| 172.29.162.146 |              1091 |               550 | x.x.x.x         |
| 172.29.162.140 |                 0 |               546 | x.x.x.x         |
| 172.29.128.117 |               282 |               499 | x.x.x.x         |
| 172.29.159.185 |               716 |               449 | x.x.x.x         |
| 172.29.64.125  |               107 |               448 | x.x.x.x         |
| 172.29.130.7   |               155 |               426 | x.x.x.x         |
| 172.29.133.69  |               569 |               423 | x.x.x.x         |
| 172.29.150.139 |               209 |               388 | x.x.x.x         |
| 172.29.155.239 |               158 |               334 | x.x.x.x         |
| 172.29.140.32  |                10 |               316 | x.x.x.x         |
+----------------+-------------------+-------------------+-----------------+
```
"""

import argparse
import subprocess
import json

from tabulate import tabulate


COMMAND = 'fdpi_ctrl list all status --service 11 --outformat json'


def get_data(command):
    """Get command output.

    Parametres
    ----------
    str:
        command

    Returns
    -------
    str:
        json in a string
    """
    command = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8',
    )

    # if command not succesfully executed, stop script
    if command.returncode != 0:
        print(f'ERROR:~ {command.stderr}')
        return False

    if not command.stdout:
        print(f'ERROR:~ Command output [{command}] is empty')
    return command.stdout


def parse_data(data, pub_ip):
    """Parse json and get rid of unnecessary data.

    Parametres
    ----------
    str:
        json in a string

    Returns
    -------
    list:
        A list of dicts
    """
    # Convert str to dict
    data = json.loads(data)

    result = []
    if pub_ip:
        for item in data['lstatuses']:
            if item['status_11']['whiteip'] == pub_ip:
                temp_user = {
                    'Private IP': item['ipv4'],
                    'TCP Utilization': item['status_11']['sess_tcp'],
                    'UDP Utilization': item['status_11']['sess_udp'],
                    'Public IP': item['status_11']['whiteip']
                    }
                result.append(temp_user)
    else:
        for item in data['lstatuses']:
            if item['status_11']['whiteip'] != '0.0.0.0':
                temp_user = {
                    'Private IP': item['ipv4'],
                    'TCP Utilization': item['status_11']['sess_tcp'],
                    'UDP Utilization': item['status_11']['sess_udp'],
                    'Public IP': item['status_11']['whiteip']
                    }
                result.append(temp_user)
    return result


def categorize_data(data, top_count):
    """Sort data and print TOP.

    Parametres
    ----------
    list:
        A list of dicts.
        {
            'Private IP': '192.168.0.1',
            'TCP Utilization': '99',
            'UDP Utilization': '1',
            'Public IP': 'x.x.x.x'
        }
    """
    sorted_by_tcp = sorted(
        data, key=lambda x: x['TCP Utilization'], reverse=True
        )[0:top_count]
    sorted_by_udp = sorted(
        data, key=lambda x: x['UDP Utilization'], reverse=True
        )[0:top_count]

    print(f"\nTOP-{top_count} port flooders by TCP")
    print(tabulate(sorted_by_tcp, headers='keys', tablefmt="psql"))
    print(f"\nTOP-{top_count} port flooders by UDP")
    print(tabulate(sorted_by_udp, headers='keys', tablefmt="psql"))


def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description="Find TCP/UDP port flooders from CGNAT.")
    parser.add_argument(
        '--top', dest='top', action='store',
        type=int, default=10, help="default TOP is 10")
    parser.add_argument(
        '--public-ip', dest='pub_ip',
        action='store', help='NAT-address')
    args = parser.parse_args()

    data = get_data(COMMAND)
    if not data:
        return False

    data = parse_data(data, args.pub_ip)
    if not data:
        return False

    categorize_data(data, args.top)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Catch CTRL+C combination
        print("Script stopped by user.")

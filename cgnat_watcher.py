#!/usr/bin/env python3

"""
cgnat_watcher.py

CGNAT has TCP/UDP port pools, cgnat-clients use these pools.
The script collects data about used TCP/UDP ports in CGNAT and sends metrics to Zabbix.


Requirements:
* python3 >=
* pip3 install py-zabbix


Usage:
```
/usr/bin/python3.6 cgnat_watcher.py --hostname x.x.x.x --command 'fdpi_ctrl list status --service 11 --profile.name cgnat_profile'
```
"""

import argparse
import subprocess
import json
import sys
import re

from pyzabbix import ZabbixMetric, ZabbixSender


def parse_output(command):
    result = []
    for line in command.strip().split('\n'):
        match = re.search(r'.*?proto=(\S+).*?nthr=(\d).*?whip=((?:\d{1,3}\.)+(?:\d{1,3})).*?prcnt_free=(\d+.\d+)', line)
        if match:
            temp_dict = {
                'protocol': match.groups()[0],
                'nthr': match.groups()[1],
                'whip': match.groups()[2],
                'prcnt_free': match.groups()[3]
            }
            result.append(temp_dict)
    result = sorted(result, key=lambda x: x['whip'])
    return result


def create_lld(result):
    lld_template = {"data": []}
    for line in result:
        temp = {"{#XSTAT_IP}": line['whip'], "{#NTHR}": line['nthr']}
        if temp not in lld_template["data"]:
            lld_template["data"].append(temp)
    return json.dumps(lld_template)


def create_metrics(hostname, result):
    metrics = []
    for line in result:
        if line["protocol"] == "TCP":
            metrics.append(
                ZabbixMetric(
                    args.hostname,
                    "xstat-nat.tcp[{0}.{1}]".format(
                        line["nthr"],
                        line["whip"]
                    ),
                    line["prcnt_free"]
                )
            )
        else:
            metrics.append(
                ZabbixMetric(
                    args.hostname,
                    "xstat-nat.udp[{0}.{1}]".format(
                        line["nthr"],
                        line["whip"]
                    ),
                    line["prcnt_free"]
                )
            )
    return metrics


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description='CGNAT port-pool watcher.')
    parser.add_argument('--hostname', required=True, action='store')
    parser.add_argument('--command', required=True, action='store')
    args = parser.parse_args()

    try:
        # Get data from fdpi_ctrl
        command = subprocess.run(
            args.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
        )

        # If command not succesfully executed, stop script
        if command.returncode != 0:
            print(command.stderr)
            sys.exit()

        # Parse data
        result = parse_output(command.stdout)

        lld_template = create_lld(result)
        metrics = create_metrics(args.hostname, result)

        zbx = ZabbixSender(
            # If value is True then default config path will be used: /etc/zabbix/zabbix_agentd.conf
            # you have to actualize that config.
            use_config=True
            )
        lld_status = zbx.send([ZabbixMetric(args.hostname, 'xstat.nat.lld', lld_template)])
        metrics_status = zbx.send(metrics)
        print("lld_status: {0}\nmetrics_status: {1}\n".format(
            lld_status, metrics_status
            )
        )
    except Exception as error:
        print(error)

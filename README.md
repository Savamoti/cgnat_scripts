# cgnat_scripts
Scripts that interact with CGNAT-soft from [VAS devs.](https://vasexperts.ru/)

## cgnat_find_flooders
The script finds TCP and UDP flooders from CGNAT service.


Requirements:
* python3.6 >=
* python3.6 -m pip install tabulate


Usage:
```
$ cgnat_find_flooders

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


## cgnat_watcher
CGNAT has TCP/UDP port pools, cgnat-clients use these pools.
The script collects data about used TCP/UDP ports in CGNAT and sends metrics to Zabbix.


Requirements:
* python3 >=
* python3.6 -m pip install py-zabbix

Usage:
```
/usr/bin/python3.6 cgnat_watcher.py --hostname x.x.x.x --command 'fdpi_ctrl list status --service 11 --profile.name cgnat_profile'
```

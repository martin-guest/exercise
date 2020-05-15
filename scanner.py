#!/usr/bin/env python3
import nmap
import sys
import json

results_filename = 'scanner_results.json'
nmap_arguments = '-Pn --unprivileged'

# check if arguments were provided
if len(sys.argv) != 2:
    sys.exit('Usage: {} {{target specification}}'.format(sys.argv[0]))

# open file with results or create empty if it does not exist
try:
    file = open(results_filename, 'r')
    json_data=file.read()
except IOError:
    file = open(results_filename, 'w')
    json_data = '{}'
    file.write(json_data)
finally:
    file.close()

last_results = json.loads(json_data)

# perform nmap scan
target = sys.argv[1]
nmScan = nmap.PortScanner()
nmScan.scan(target,arguments=nmap_arguments)

# check results for each target host
results = {}
for host in nmScan.all_hosts():
    changed = False
    output = []
    results[host] = {}
    for proto in nmScan[host].all_protocols():
        lport = sorted(nmScan[host][proto].keys())
        for port in lport:
            state = nmScan[host][proto][port]['state']
            # check if port was open in last scan
            if str(port) not in last_results.get(host,{}).get(proto,{}).keys():
                changed = True
            # check if port state was different in last scan
            elif state != last_results.get(host,{}).get(proto,{}).get(str(port)):
                changed = True
            # prepare output
            output.append('Host: %s Ports: %s/%s/%s////' % (host.ljust(16),port,state,proto))
            # add port to results
            entry = { str(port): state }
            if proto not in results[host].keys():
                results[host] = { proto: {} }
            results[host][proto].update(entry)
    # check if ports were closed by comparing results to last result
    if last_results.get(host) != results.get(host):
        changed = True
    # print results for target host
    if changed:
        print('*Target - %s: Full scan results:*' % (host))
        print('\n'.join(output))
    else:
        print('*Target - %s: No new results in the last scan.*' % (host))

# update last results and write to file
last_results.update(results)

last_results_json = json.dumps(last_results)
file = open(results_filename,"w")
file.write(last_results_json)
file.close()

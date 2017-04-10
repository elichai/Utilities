from collections import Counter

import requests

snapshots = requests.get('https://getaddr.bitnodes.io/api/v1/snapshots/')
counter = Counter()
all = {'BU': Counter(), 'UASF': Counter(), 'Classic': Counter(), 'XT': Counter(), 'Core': Counter(), 'Other': Counter()}
ips = set()
for result in snapshots.json()['results']:
    page = requests.get(result['url'])
    for ip, node in page.json()['nodes'].items():
        if ip in ips:
            continue
        ips.add(ip)
        counter['total'] += 1
        node = node[1]
        if 'uasf' in node.lower() or 'usaf' in node.lower():
            counter['UASF'] += 1
            all['UASF'][node] += 1
        elif 'unlimited' in node.lower():
            counter['BU'] += 1
            all['BU'][node] += 1
        elif 'eb3.7' in node.lower() or 'classic' in node.lower() or '1.2.3' in node.lower():
            counter['Classic'] += 1
            all['Classic'][node] += 1
        elif 'XT' in node:
            counter['XT'] += 1
            all['XT'][node] += 1
        elif 'satoshi' in node.lower() or 'bcoin' in node.lower() or 'statoshi' in node.lower():
            counter['Core'] += 1
            all['Core'][node] += 1

        else:
            counter['Other'] += 1
            all['Other'][node] += 1

for key, value in counter.items():
    print key, ': ', value

for key, value in all.items():
    print key, ':'
    for a, b in value.items():
        print a, ': ', b

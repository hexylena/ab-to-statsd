#!/usr/bin/env python
"""
Parse json files from another tool and send to statsd
"""
import statsd
import subprocess
import json

REPEAT_COUNT = 30

data = {
    'cpt-tamu-edu': [
        ['landing', 'https://cpt.tamu.edu/'],
        ['owncloud', 'https://cpt.tamu.edu/owncloud/'],
    ]
}

c = statsd.StatsClient('biobio-monitor.tamu.edu', 8125)
for site in data:
    for (name, url) in data[site]:
        command = ['boom', '-m', 'GET', '--json-output', '-n',
                   str(REPEAT_COUNT), url]
        output = subprocess.check_output(command)
        data = json.loads(output)
        for key in data:
            stat_name = 'page_load.%s.%s.%s' % (site, name, key)
            c.gauge(stat_name, data[key])

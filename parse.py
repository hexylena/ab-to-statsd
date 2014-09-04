#!/usr/bin/env python
"""
Parse json files from another tool (boom) and send to statsd
"""
import statsd
import subprocess
import json
import yaml

with open('conf.yaml', 'r') as handle:
    data = yaml.load(handle)

c = statsd.StatsClient(data['global']['statsd']['host'],
                       data['global']['statsd']['port'])
for site in data['urls']:
    for (name, url) in data['urls'][site]:
        command = ['boom', '-m', 'GET', '--json-output', '-n',
                   str(data['global']['requests']), url]
        output = subprocess.check_output(command)
        ab_data = json.loads(output)
        for key in ab_data:
            stat_name = 'page_load.%s.%s.%s' % (site, name, key)
            print "%s %s" % (stat_name, ab_data[key])
            c.gauge(stat_name, data[key])

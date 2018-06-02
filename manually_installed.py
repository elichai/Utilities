from subprocess import check_output
import requests

list_manual = set(check_output(['apt-mark', 'showmanual']).split('\n'))

online = requests.get('http://releases.ubuntu.com/releases/yakkety/ubuntu-16.10-desktop-amd64.manifest').text
online = set(str(online).split('\n'))

preinstalled = set()
for one in online:
    preinstalled.add(one.split('\t')[0])

list_manual = list_manual - preinstalled

for i in sorted(list_manual):
    print i

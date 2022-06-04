import os
import time
import datetime as dt
import requests

bscount = 7
offline = 0

r = requests.get('https://10.0.0.1:2000/')
if not r.status_code == 200:
    offline = 1

if offline == 1:
    response = requests.post('https://api.telegram.org/[token]/sendMessage',
    data={
        'chat_id': '[chat_ID]',
        'text': 'PfSense-Backup Failed!'
    }
)
    time.sleep(2)
    exit()

os.system('ssh admin@10.0.0.1 cat /cf/conf/config.xml > ./backup/tmp-backup.xml')
time.sleep(2)
x = dt.datetime.now()
now = str(x.date())
dateiname = now + '.xml'
os.rename('./backup/tmp-backup.xml', './backup/' + dateiname)

dir = './backup'
initial_count = 0
for path in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, path)):
        initial_count += 1
#print(initial_count)

if initial_count < bscount:
    True
else:
    oldest_file = sorted([ "./backup/"+f for f in os.listdir("./backup/")], key=os.path.getctime)[0]
    #print(oldest_file)
    os.remove(oldest_file)

import os
import socket

baseDir = os.path.dirname(os.getcwd())
benighIP = []
count = 0
with open(os.path.join(baseDir, 'processedData', 'intervalResultdata.txt')) as fRead:
    for line in fRead:
        count += 1
        print(str(count)+"/444")
        domain = line.split(' ')[1]
        try:
            ip = socket.gethostbyname(domain)
        except:
            continue
        if ip!='114.114.114.114':
            benighIP.append(domain)
print('---------------------------------------')
print(benighIP)
print(len(benighIP))

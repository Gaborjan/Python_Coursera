import urllib.request, urllib.parse, urllib.error
import json
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    url = input('Enter URL: ')
    if len(url) < 1: break

    print('Retrieving', url)
    uh = urllib.request.urlopen(url)
    data = uh.read()

    print('Retrieved', len(data), 'characters')
    print(data.decode())

    info=json.loads(data)
    print('Count: ',len(info['comments']))
    sum_of_comments=0
    for item in info['comments']:
        sum_of_comments=sum_of_comments+item['count']
    print('Sum: ',sum_of_comments)        
        
   

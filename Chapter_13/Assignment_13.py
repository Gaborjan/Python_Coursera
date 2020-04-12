import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url =  "http://py4e-data.dr-chuck.net/comments_361884.xml"
print('Retrieving', url)
uh = urllib.request.urlopen(url)
data = uh.read()
print('Retrieved', len(data), 'characters')

tree = ET.fromstring(data)
data = tree.findall('comments/comment')
sum_of_comments=0
for item in data:
    sum_of_comments=sum_of_comments+int(item.find('count').text)

'''
data=tree.findall('.//count')
for item in data:
    sum_of_comments=sum_of_comments+int(item.text)
    users=users+1
'''

print('Count: ',len(data))
print('Sum: ',sum_of_comments)





       

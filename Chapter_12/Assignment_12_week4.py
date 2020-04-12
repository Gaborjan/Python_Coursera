# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the <span> tags
counter=0 #number of the <span> tags
sum_span=0 #sum of <span> contents
tags = soup('span')
for tag in tags:
    #print('Contents:', tag.contents[0])
    counter=counter+1
    sum_span=sum_span+int(tag.contents[0])
print('Count',counter)
print('Sum of span content:',sum_span)

    
   

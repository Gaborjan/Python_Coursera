import re
f=open('regex_sum_361880.txt','r')
print(sum([int(x) for x in re.findall('[0-9]+',f.read())]))
f.close()



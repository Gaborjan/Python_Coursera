import xml.etree.ElementTree as ET

input='''
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>  '''

tree=ET.fromstring(input)
lst=tree.findall('./country')
for item in lst:
    print('Ország: ',item.get('name'))
    print('Év: ',item.find('year').text)
    print('GDP/fő: ',item.find('gdppc').text,'$')
    neighbors=item.findall('neighbor')
    for item1 in neighbors:
        print('Szomszéd ország: ',item1.get('name'),item1.get('direction'))

'''lst=tree.findall('./country/neighbor')
for item in lst:
    print(item.get('name'))

lst1=tree.findall(".//year/..[@name='Singapore']")
for item in lst1:
    print(item.find('gdppc').text)

lst2=tree.findall(".//neighbor")
for item in lst2:
    print(item.get('name'))'''
    

    

import json
input='''[
    {
        "id":"001",
        "x":"2",
        "name":"Chuck"
    },
    {
        "id":"009",
        "x":"7",
        "name":"Gabika"
    }
]'''

info=json.loads(input)
print(type(info))
print('User count:',len(info))
for item in info:
    print(type(item))
    print('Name:',item["name"])
    print('Id:',item["id"])
    print('Attribute:',item["x"])
    
    
    
    

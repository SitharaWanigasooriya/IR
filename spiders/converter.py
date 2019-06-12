import json

with open('/home/sithara/Virtual Enviornments/Info_Ret/crawler/crawler/baiscope_unicode.json') as ob:
    data = json.load(ob)

with open('/home/sithara/Virtual Enviornments/Info_Ret/crawler/crawler/baiscope_sinhala.json', 'w') as ob1:
    json.dump(data, ob1, ensure_ascii=False)
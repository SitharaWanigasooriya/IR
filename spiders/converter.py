import json

with open('/home/sithara/Virtual Enviornments/Info_Ret/crawler/crawler/baiscope_unicode_moreTags.json') as ob:
    data = json.load(ob)

with open('/home/sithara/Virtual Enviornments/Info_Ret/crawler/crawler/baiscope_sinhala_moreTags.json', 'w') as ob1:
    json.dump(data, ob1, ensure_ascii=False)
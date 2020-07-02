import json

with open('douban_top250.json','r',encoding='utf-8') as f1:
    content=[]
    for line in f1.readlines():
        content.append(json.loads(line))

content.sort(key=lambda x: int(x["result"]["ranking"][3:]))

with open('douban_movie_top250.json','w',encoding='utf-8') as f2:
    f2.write(json.dumps(content,indent=4,ensure_ascii=False))

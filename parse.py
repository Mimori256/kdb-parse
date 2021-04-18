import json


with open("ukdb.csv", "r", encoding="utf_8") as f:
    l=[]
    for i in range(19075):
        tmp = f.readline().split('"')

        if tmp[15] == "":
            tmp[15] = " " 

        if not "" in set([tmp[1], tmp[3], tmp[11], tmp[13], tmp[15], tmp[21]]):
            l.append([tmp[1], tmp[3], tmp[11], tmp[13], tmp[15], tmp[21]])

json_data = []
l.pop(0)

for data in l:
    json_data.append({"id": data[0], "name": data[1], "module": data[2], "period": data[3], "room": data[4], "note": data[5]})

enc = json.dumps(json_data, indent=2, ensure_ascii=False)

with open("kdb.json", "w") as f:
    f.write(enc)

print("complete")

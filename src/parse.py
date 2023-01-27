import json

# Parse csv to kdb.json
with open("kdb.csv", "r", encoding="utf_8") as f:
    l = []
    lines = f.readlines()
    # remove the header
    lines.pop(0)
    for line in lines:
        tmp = line.split('"')
        class_id = tmp[1]
        name = tmp[3]
        module = tmp[11]
        period = tmp[13]
        room = tmp[15]
        remarks = tmp[21]

        if room == "":
            room = " "

        unit = tmp[7]
        unit = unit.replace(" ", "")
        class_data = [class_id, name, module, period, room, remarks, unit]

        if not "" in set(class_data):
            l.append(class_data)

json_data = {}
l.pop(0)

for i in l:
    json_data[i[0]] = i[1:]

# { "科目番号": ["科目名","モジュール","曜時限","教室","備考","単位数"], ・・・}
enc = json.dumps(json_data, ensure_ascii=False, indent=2)

with open("kdb.json", "w") as f:
    f.write(enc)

print("complete")

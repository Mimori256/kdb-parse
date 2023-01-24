import json

# Parse csv to kdb.json
with open("kdb.csv", "r", encoding="utf_8") as f:
    l = []
    lines = f.readlines()
    # remove the header
    lines.pop(0)
    for line in lines:
        tmp1 = line.split('"')

        if tmp1[15] == "":
            tmp1[15] = " "

        unit = tmp1[7]
        unit = unit.replace(" ", "")
        if not "" in set(
            [tmp1[1], tmp1[3], tmp1[11], tmp1[13], tmp1[15], tmp1[21], unit]
        ):
            l.append([tmp1[1], tmp1[3], tmp1[11], tmp1[13], tmp1[15], tmp1[21], unit])

json_data = {}
l.pop(0)

for i in l:
    json_data[i[0]] = i[1:]

# { "科目番号": ["科目名","モジュール","曜時限","教室","備考","単位数"], ・・・}
enc = json.dumps(json_data, ensure_ascii=False, indent=2)

with open("kdb.json", "w") as f:
    f.write(enc)

print("complete")

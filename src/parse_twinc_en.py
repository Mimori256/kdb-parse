import json
import re

# Global consts
global WEEKDAY_LIST, SEASONS, MODULE_LIST, SPRING_MODULE_LIST, FALL_MODULE_LIST, SPECIAL_MODULE_LIST
WEEKDAY_LIST = ["月", "火", "水", "木", "金", "土", "日"]
SEASONS = ["春", "秋"]
MODULE_LIST = ["春A", "春B", "春C", "秋A", "秋B", "秋C", "夏季休業中", "春季休業中"]
SPRING_MODULE_LIST = ["春A", "春B", "春C"]
FALL_MODULE_LIST = ["秋A", "秋B", "秋C"]
SPECIAL_MODULE_LIST = ["夏季休業中", "春季休業中"]


class Class:
    def __init__(self, class_id, name, module, period_tmp, room, description):
        self.class_id = class_id
        self.name = name
        self.module = module
        self.period_tmp = period_tmp
        self.room = room
        self.description = description
        self.terms = []
        self.period = []

    def as_json(self):
        return {
            "class_id": self.class_id,
            "name": self.name,
            "module": self.terms,
            "period": self.period,
            "room": self.room,
            "description": self.description,
        }

    def parsed_module(self):
        module = self.terms
        for i in range(len(module)):
            res = []
            special_module_list = []
            spring_table = [False, False, False]
            fall_table = [False, False, False]
            for j in range(len(module[i])):
                if module[i][j] in SPRING_MODULE_LIST:
                    spring_table[SPRING_MODULE_LIST.index(module[i][j])] = True
                elif module[i][j] in FALL_MODULE_LIST:
                    fall_table[FALL_MODULE_LIST.index(module[i][j])] = True
                # 夏季休業中 or 春季休業中
                else:
                    special_module_list.append(module[i][j])

            if any(spring_table):
                res.append(check_table(spring_table, "春"))
            if any(fall_table):
                res.append(check_table(fall_table, "秋"))

            for element in special_module_list:
                res.append(element)

            module[i] = res

        return module


def check_table(table, season):

    ABC_LIST = ["A", "B", "C"]
    module = ""
    if any(table):
        module = season
        for i in range(len(table)):
            if table[i]:
                module += ABC_LIST[i]
        return module


def create_class_list():

    with open("kdb.csv", "r", encoding="utf_8") as f:
        class_list = []
        lines = f.readlines()

        # Remove the header
        lines.pop(0)

        for line in lines:
            tmp = line.split('"')
            class_id = tmp[1]
            name = tmp[31]
            module = tmp[11]
            period_tmp = tmp[13]
            room = tmp[15]
            description = tmp[21]

            if room == "":
                room = " "

            # Remove classes that are not opened in this year
            if not "" in set([class_id, name, module, period_tmp, room, description]):
                class_list.append(
                    Class(class_id, name, module, period_tmp, room, description)
                )

        return class_list


def create_timetable():
    timetable = []
    for i in range(7):
        timetable.append([False for i in range(8)])
    return timetable


def parse_timetable(table):

    blank_table = create_timetable()
    period = ""
    period_list = []

    if table["period"] == blank_table:
        if table["focus"]:
            return ["集中"]
        elif table["negotiable"]:
            return ["応談"]
        else:
            return ["随時"]

    for i in range(7):
        for j in range(8):
            if table["period"][i][j]:
                period = WEEKDAY_LIST[i] + str(j + 1)
                period_list.append(period)

    return period_list


subject_map = {}

class_list = create_class_list()

for course in class_list:

    term_groups = course.module.split(" ")
    season = ""

    for group_str in term_groups:
        group = []
        char_array = list(group_str)

        for char in char_array:

            if char in SEASONS:
                season = char

            if season != "":
                if char in ["A", "B", "C"]:
                    if season == "春":
                        no = 0
                    else:
                        no = 3

                    if char == "A":
                        no += 0
                    elif char == "B":
                        no += 1
                    else:
                        no += 2
                    group.append(no)

                if char == "休":
                    group.append(SEASONS.index(season) + 6)

        group = list(map(lambda x: MODULE_LIST[x], group))
        course.terms.append(group)

    term_str_array = course.period_tmp.split(" ")

    for i in range(len(term_str_array)):
        term = term_str_array[i]
        period_str_array = term.split(",")
        day_array = []
        course.period.append(
            {
                "focus": term.find("集中") > -1,
                "negotiable": term.find("応談") > -1,
                "asneeded": term.find("随時") > -1,
                "period": create_timetable(),
            }
        )

        for p in period_str_array:
            day_str = re.sub("[0-9\-]", "", p)
            days = day_str.split("・")
            days = list(filter(lambda x: x in WEEKDAY_LIST, days))
            days = list(map(lambda x: WEEKDAY_LIST.index(x), days))

            if len(days) > 0:
                day_array = days

            time_array = []
            time_str = re.sub("[^0-9\-]", "", p)

            if time_str.find("-") > -1:
                time_str_array = time_str.split("-")
                start_time = int(time_str_array[0])
                end_time = int(time_str_array[1])
                for j in range(start_time, end_time + 1, 1):
                    time_array.append(j)

            else:
                if time_str != "":
                    time_array.append(int(time_str))
                else:
                    time_array.append("")

            if len(time_str) > 0:
                for day in day_array:
                    for time in time_array:
                        course.period[i]["period"][day][time - 1] = True

    for i in range(len(course.period)):
        course.period[i] = parse_timetable(course.period[i])

    course.terms = course.parsed_module()

    if course.terms == [[]]:
        course.terms = [["通年"]]

    subject_map[course.class_id] = course.as_json()

enc = json.dumps(subject_map, ensure_ascii=False)
with open("kdb_twinc_en.json", "w") as f:
    f.write(enc)
print("complete")

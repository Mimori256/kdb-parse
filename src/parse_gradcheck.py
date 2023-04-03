import json
import csv


def csv_to_dict():
    courses = {"courses": []}
    with open("kdb.csv", "r", encoding="utf_8") as f:
        reader = csv.reader(f)
        once = False
        for row in reader:
            if not once:
                once = True
                continue
            course_data = {}
            course_data["id"] = row[0].strip()
            course_data["name"] = row[1].strip()
            course_data["credits"] = row[3].strip()
            course_data["modules"] = row[5].strip()
            course_data["period"] = row[6].strip()
            courses["courses"].append(course_data)

    return courses


def main():
    courses = csv_to_dict()
    with open("kdb_gradcheck.json", "w") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    print("complete")


if __name__ == "__main__":
    main()

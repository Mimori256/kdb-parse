import json
import csv


def csv_to_dict() -> dict[str, list[dict[str, str]]]:
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
            course_data["method"] = row[2].strip()
            course_data["credits"] = row[3].strip()
            course_data["standard_course_year"] = row[4].strip()
            course_data["modules"] = row[5].strip()
            course_data["period"] = row[6].strip()
            course_data["classroom"] = row[7].strip()
            course_data["teaching_staff"] = row[8].strip()
            course_data["class_outline"] = row[9].strip()
            course_data["note"] = row[10].strip()
            course_data["application_for_enrollment"] = row[11].strip()
            course_data["application_requirements_for_enrollment"] = row[12].strip()
            course_data["application_for_short_term_international_students"] = row[
                13
            ].strip()
            course_data[
                "application_requirements_for_short_term_international_students"
            ] = row[14].strip()
            course_data["english_course_name"] = row[15].strip()
            course_data["course_code"] = row[16].strip()
            course_data["requirement_course_name"] = row[17].strip()
            course_data["data_update_date"] = row[18].strip()
            courses["courses"].append(course_data)

    return courses


def main():
    courses = csv_to_dict()
    with open("kdb_structural.json", "w") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    print("complete")


if __name__ == "__main__":
    main()

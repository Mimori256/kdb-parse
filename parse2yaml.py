import yaml

from parse_structural import csv_to_dict


def main():
    courses = csv_to_dict()
    with open("kdb.yaml", "w") as f:
        yaml.dump(courses, f, allow_unicode=True)

    print("complete")


if __name__ == "__main__":
    main()

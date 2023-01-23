import csv
import json
from enum import Enum
import xml.etree.ElementTree as ET


def getTranslations(lang):
    with open("translations.json", "r", encoding="utf_8") as f:
        trans = json.load(f)
        return trans[lang]


def str2tagName(str):
    return str.lower().replace(" ", "_").replace("(", "").replace(")", "")


def courseEnum(lang):
    with open("csvHeader.json", "r", encoding="utf_8") as f:
        cols = json.load(f)
        return Enum("Course", cols[lang], start=0)


def insertAttrElement(parent, name, value):
    child = ET.SubElement(parent, str2tagName(name))
    child.text = value
    return child


def csv2xml(reader, Course, lang):
    # remove the header
    next(reader)
    root = ET.Element(getTranslations(lang)["courses"])
    for course in reader:
        courseElement = ET.SubElement(root, getTranslations(lang)["course"])
        for attr in map(lambda x: x.name, Course):
            insertAttrElement(
                parent=courseElement, name=attr, value=course[Course[attr].value]
            )

    return root


def main(input, output, lang="ja"):
    Course = courseEnum(lang)

    with open(input, "r", encoding="utf_8") as f:
        reader = csv.reader(f)
        root = csv2xml(reader, Course, lang)

    with open(output, "w") as f:
        f.write(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    main("kdb.csv", "kdb.xml")

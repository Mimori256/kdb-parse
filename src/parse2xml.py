import csv
import json
import xml.etree.ElementTree as ET
from enum import Enum


def getTranslations(lang: str) -> dict[str, str]:
    with open("translations.json", "r", encoding="utf_8") as f:
        trans: dict[str, dict[str, str]] = json.load(f)
        return trans[lang]


def str2tagName(str: str) -> str:
    return str.lower().replace(" ", "_").replace("(", "").replace(")", "")


def courseEnum(lang: str) -> Enum:
    with open("csvHeader.json", "r", encoding="utf_8") as f:
        cols: dict[str, list[str]] = json.load(f)
        return Enum("Course", cols[lang], start=0)


def insertAttrElement(parent: ET.Element, name: str, value: str) -> ET.Element:
    child = ET.SubElement(parent, str2tagName(name))
    child.text = value
    return child


def csv2xml(reader, Course, lang: str) -> ET.Element:
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


def main(input: str, output: str, lang: str):
    Course = courseEnum(lang)

    with open(input, "r", encoding="utf_8") as f:
        reader = csv.reader(f)
        root = csv2xml(reader, Course, lang)

    with open(output, "w") as f:
        f.write(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    main("kdb.csv", "kdb.xml", "ja")

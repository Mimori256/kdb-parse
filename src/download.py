import os
import datetime
import requests
import urllib.parse

now = datetime.datetime.now()
year = now.year
month = now.month

if month < :
    nendo = year - 1

else:
    nendo = year

post = {
    "index": "",
    "locale": "",
    "nendo": nendo,
    "termCode": "",
    "dayCode": "",
    "periodCode": "",
    "campusCode": "",
    "hierarchy1": "",
    "hierarchy2": "",
    "hierarchy3": "",
    "hierarchy4": "",
    "hierarchy5": "",
    "freeWord": "",
    "_orFlg": 1,
    "_andFlg": 1,
    "_gaiyoFlg": 1,
    "_risyuFlg": 1,
    "_excludeFukaikoFlg": 1,
}

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"

kdb_url = "https://kdb.tsukuba.ac.jp/"
session = requests.session()
response = session.get(kdb_url)

if response.status_code != 200:
    raise ValueError("Connection Error")


do_url = response.url
qs = urllib.parse.urlparse(do_url).query
query_dict = urllib.parse.parse_qs(qs)

# search
search_post = post.copy()
search_post["_eventId"] = "searchOpeningCourse"
response = session.post(do_url, data=search_post)
do_url = response.url

# download a csv
csv_post = post.copy()
csv_post["_eventId"] = "output"
csv_post["outputFormat"] = 0
response = session.post(do_url, data=csv_post)

# output
with open("tmp.csv", "w", encoding="utf-8") as fp:
    fp.write(response.text)

# compare file
try:
    original = open("kdb.csv", "r", encoding="utf-8")
except:
    os.rename("tmp.csv", "kdb.csv")
    print("CSV updated")
    exit()



changed = open("tmp.csv", "r", encoding="utf-8")

# no change
if original == changed:
    os.remove("tmp.csv")
    print("No change")

else:
    print("CSV updated")
    os.remove("kdb.csv")
    os.rename("tmp.csv", "kdb.csv")

original.close()
changed.close()

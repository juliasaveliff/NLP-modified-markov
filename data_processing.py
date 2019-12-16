import json

with open("data_2019.json") as file:
    data = json.load(file)
# data = json.load(uploaded['data_2019.json'])
body = []
titles=[]
categories = {}

for item in data["2019"]:
    if item["category"] not in categories:
        categories[item["category"]] = []
    # categories[item["category"]].append(item)

    # body = body + item["content"].split()
    # titles = titles+ item["title"].split()
    # titles.append(".")



import re
data_opinion = []
for item in categories["Opinion"]:
    data_processed = re.findall(r"[\w'’]+|[.,!?;]", item["content"])
    data_opinion = data_opinion + data_processed
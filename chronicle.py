import glob
import json 
import re
year_dirs= glob.glob("html/www.dukechronicle.com/article/*")

output_file= "data.json"
years = []
for year in year_dirs:
	temp = year.split("/")
	year_num = temp[-1]
	try:
		int(year_num)
		years.append(year_num)
	except:
		pass



data = {}

for year in sorted(years):
	year_data = []
	month_dirs = glob.glob("html/www.dukechronicle.com/article/" + year + "/*")
	for month in month_dirs:
		files = glob.glob(month + "/*")
		for file in files:
			file_dict = {}
			f = open(file,'r')
			f_data = f.read()
			title = re.findall("(?<=<title>)[a-zA-Z0-9_.-].*(?= - The Chronicle<\/title)",f_data)
			content_1 = re.findall("(?<=<p>)[“a-zA-Z0-9_.-].*(?=&nbsp;<\/p)|(?<=<p>)[“a-zA-Z0-9_.-].*(?=<\/p)",f_data)
			try:
				if content_1[-1] == 'Signup for our editorially curated, weekly newsletter. Cancel at any time.':
					content_1.pop()
			except:
				print(file)
			content = re.findall("[^<>]*(?=<a|<\/a)|(?<=a>)[^<>]*", "<a>" + " ".join(content_1) + "</a>")
			content = " ".join(content)
			category = re.findall("(?<=articleSection\": \")[A-Za-z, ]*(?=\",)",f_data)
			date = re.findall("(?<=dateCreated\": \")[0-9\-A-Za-z,: ]*(?=\",)",f_data)

			file_dict["title"] = " ".join(title)
			file_dict["category"] = " ".join(category)
			file_dict["date"] = " ".join(date)
			file_dict["content"] = content
			year_data.append(file_dict)
	data[year] = year_data

with open(output_file, "w") as out:
	json.dump(data,out,indent = " ")


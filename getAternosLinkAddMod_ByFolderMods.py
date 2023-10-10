PATH_MODS = "/home/vespan/.minecraft/mods/"

import requests
import json
import os
import re

mods = {
	"failed": [],
	"insert": [],
	"checked": [],
}

def matchModFilename(text):
	r = [
		r'^(\w+)[\-\_\+](\w+)[\-\_\+]\d',
		r'^(\w+)[\-\_\+]\d',
		r'^(\w+)[\-\_\+]\w\d',
		r'^(\w+)[\-\_\+]mc\d',
	]
	for i in range(0,len(r)):
		ret = re.search(r[i],text)
		if ret:
			if i == 0:
				return ret[1] + "_" + ret[2]
			else:
				return ret[1]

	return None

def searching(text,pattern):
    def getWord(text):
        res = [""]
        index = 0
        for v in text:
            if re.search(r'[\!\"\#\$\%\&\'\(\)\*\+\-\.\/\:\;\<\=\>\?\@\[\]\^\_\`\{\}\|\~]',v):
                index += 1
                res.append("")
            else:
                res[index] += v
        return res
    finding = 0
    l = getWord(pattern)
    for w in l:
        if re.search(w,text):
            finding += 1

    return (finding==len(l)),finding



mylist = os.listdir(PATH_MODS)
for v in mylist:
	mm = matchModFilename(v)
	if mm:
		mods["insert"].append(mm)
	else:
		mods["failed"].append(v)

def parsing(rj):
	for v in rj["data"]:
		if v["class"]["name"] == 'Mods':
			for websiteRecentFiles in v["websiteRecentFiles"]:
				for files in websiteRecentFiles["files"]:
					search,index = searching(files["fileName"],mod)
					if search:
						print(mod,"https://aternos.org/addons/a/curseforge/"+v["slug"])
						mods["checked"].append("https://aternos.org/addons/a/curseforge/"+v["slug"])
						return
	return

for mod in mods["insert"]:
	r = requests.get("https://www.curseforge.com/api/v1/mods/search?gameId=432&index=0&filterText="+mod+"&pageSize=20&sortField=1")
	if r.status_code == 200:
		rj = json.loads(r.text)
		parsing(rj)

	else:
		print('error status_code')

path = "aternos/"
if not os.path.exists(path):
    os.mkdir(path)

with open("res.txt","w") as f:
	text = ""
	for failed in mods["failed"]:
		text = text + "\nFAILED:" + failed

	text += "\n\n"

	for checked in mods["checked"]:
		text = text + "\n" + checked
	f.write(text)
	f.close()

for checked in mods["checked"]:
	r = checked.replace("https://aternos.org/addons/a/curseforge/","")
	with open(path+r+".bat","w") as bat:
		bat.write(" start \"\" "+checked+"\ndel %~f0")
		bat.close()
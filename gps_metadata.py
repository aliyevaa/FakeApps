from GPS import GPStore
import json

def get_info(p,packages):
	info = {}
	print(len(packages["topFree"]))
	for cat in packages:
		for i in packages[cat]:
			app = {}
			print(i)
			stats = p.get_stats(i)
			app["title"] = stats["title"]
			app["icon_url"] = stats["icon"]
			app["desc"] = stats["description"]
			app["dEmail"] = stats["developerEmail"]
			app["d"] = stats["developer"]
			app["pp"] = stats["privacyPolicy"]
			app["dWebsite"] = stats["developerWebsite"]
			app["category"] = cat
			app["version"] = stats["version"]
			app["released"] = stats["released"]
			app["size"] = stats["size"]
			app["name"] = p.get_name(i)
			if "@string" in app["name"]:
				app["name"] = ""
			print(app["name"])
			info[i] = app
	js = json.dumps(info)
	with open("GPS_appsTopFreeMeta", "a") as g:
		g.write(js)
	#p.done()


def main():	
	url = "https://play.google.com/store/apps/collection/cluster?clp=0g4jCiEKG3RvcHNlbGxpbmdfZnJlZV9BUFBMSUNBVElPThAHGAM%3D:S:ANO1ljKs-KA&gsr=CibSDiMKIQobdG9wc2VsbGluZ19mcmVlX0FQUExJQ0FUSU9OEAcYAw%3D%3D:S:ANO1ljL40zU"
	p = GPStore(url)
	packages = p.get_packages()
	get_info(p,packages)
	p.done()


main()

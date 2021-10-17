import json
import requests
import threading

def update_check(app, silent=True):
	try:
		latest = json.loads(requests.get("https://api.github.com/repos/TheQuinbox/quinread/releases/latest",{"accept":"application/vnd.github.v3+json"}).content.decode())
		if app.version < latest["tag_name"]:
			ud = question("Update available: " + latest["tag_name"],"There is an update available. Your version: " + app.version + ". Latest version: " + latest["tag_name"] + ". Description: " + latest["body"] + "\r\nDo you want to open the direct download link?")
			if ud == 1:
				for i in latest["assets"]:
					if "quinread.zip" in i["name"].lower():
						threading.Thread(target=download_update, args=[i["browser_download_url"],], daemon=True).start()
						return
		else:
			if not silent:
				alert("No updates available! The latest version of the program is " + latest["tag_name"],"No update available")
	except:
		pass

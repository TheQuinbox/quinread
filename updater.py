import json
import requests
import webbrowser
import wx

def update_check(app, silent):
	try:
		latest = json.loads(requests.get("https://api.github.com/repos/TheQuinbox/quinread/releases/latest",{"accept":"application/vnd.github.v3+json"}).content.decode())
		if app.version < latest["tag_name"]:
			dlg=wx.MessageDialog(app.main_frame, "There is an update available. Your version: " + app.version + ". Latest version: " + latest["tag_name"] + ". Description: " + latest["body"] + "\nDo you want to open the direct download link?", "Update available: " + latest["tag_name"], wx.YES_NO | wx.ICON_QUESTION)
			result=dlg.ShowModal()
			dlg.Destroy()
			if result == wx.ID_YES:
				webbrowser.open(i["browser_download_url"])
		else:
			if not silent:
				wx.MessageBox("No updates available! The latest version of the program is " + latest["tag_name"], "No update available")
	except Exception as e:
		raise e

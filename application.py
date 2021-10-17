import wx
from gui import main
import custom_tweak
import os
import updater

class Application:
	def __init__(self):
		self.name = "Quinread"
		self.version = "0.40"
		self.running = False
		self.config = None
		self.load_config()
		self.wx = wx.App()
		self.main_frame = main.MainFrame(self)
		updater.update_check(self, True)

	def run(self):
		self.running = True
		self.main_frame.Show()
		self.wx.MainLoop()

	def load_config(self):
		self.config = custom_tweak.Config(name=self.name, autosave=True, custom_path=os.getcwd())
		self.config.loaded_documents = self.config.get("loaded_documents", {})
		self.config.last_loaded_path = self.config.get("last_loaded_path", "")
		self.config.last_loaded_filename = self.config.get("last_loaded_filename", "")
		self.config.load_previous = self.config.get("load_previous", True)

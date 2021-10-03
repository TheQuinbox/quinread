import wx
from gui import main
import custom_tweak
import os

class Application:
	def __init__(self):
		self.name = "Quinread"
		self.version = "0.1"
		self.running = False
		self.config = None
		self.load_config()
		self.wx = wx.App()
		self.main_frame = main.MainFrame(self)

	def run(self):
		self.running = True
		self.main_frame.Show()
		self.wx.MainLoop()

	def load_config(self):
		self.config = custom_tweak.Config(name=self.name, autosave=True, custom_path=os.getcwd())
		self.config.loaded_documents = self.config.get("loaded_documents", {})

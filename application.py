import wx
from gui import main

class Application:
	def __init__(self):
		self.name = "Quinread"
		self.version = "0.10"
		self.running = False
		self.wx = wx.App()
		self.main_frame = main.MainFrame(self)

	def run(self):
		self.running = True
		self.main_frame.Show()
		self.wx.MainLoop()

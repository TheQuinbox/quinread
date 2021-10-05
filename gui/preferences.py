import wx

class PreferencesDialog(wx.Dialog):
	def __init__(self, app):
		self.app = app
		wx.Dialog.__init__(self, None, title="Preferences", size=wx.DefaultSize)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.load_previous = wx.CheckBox(self, -1, "&Load previously loaded document on startup")
		self.main_box.Add(self.load_previous, 0, wx.ALL, 10)
		self.load_previous.SetValue(self.app.config.load_previous)
		self.ok = wx.Button(self.panel, wx.ID_OK, "&OK")
		self.main_box.Add(self.ok, 0, wx.ALL, 10)
		self.ok.Bind(wx.EVT_BUTTON, self.on_ok)
		self.ok.SetDefault()
		self.cancel = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.main_box.Add(self.cancel, 0, wx.ALL, 10)
		self.cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
		self.Bind(wx.EVT_CLOSE, self.on_cancel)
		self.panel.Layout()

	def on_ok(self, event=None):
		self.app.config.load_previous = self.load_previous.GetValue()
		self.Destroy()

	def on_cancel(self, event=None):
		self.Destroy()

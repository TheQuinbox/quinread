import wx

class GotoDialog(wx.Dialog):
	def __init__(self, frame):
		self.frame = frame
		wx.Dialog.__init__(self, None, title="Goto", size=wx.DefaultSize)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "&Line")
		self.main_box.Add(self.text_label, 0, wx.ALL, 10)
		self.text_field = wx.TextCtrl(self.panel, size=(600, 600))
		self.main_box.Add(self.text_field, 0, wx.ALL, 10)
		self.text_field.SetValue(f"{self.get_current_line()}")
		self.go = wx.Button(self.panel, wx.ID_OK, "&Go")
		self.main_box.Add(self.go, 0, wx.ALL, 10)
		self.go.Bind(wx.EVT_BUTTON, self.on_go)
		self.go.SetDefault()
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Close")
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.close.Bind(wx.EVT_BUTTON, self.on_close)
		self.Bind(wx.EVT_CLOSE, self.on_close)
		self.panel.Layout()
	
	def get_current_line(self):
		return len(self.frame.reader.GetRange(0, self.frame.reader.GetInsertionPoint()).split("\n"))
	
	def on_close(self, event=None):
		self.Destroy()
	
	def on_go(self, event=None):
		try:
			line = int(self.text_field.GetValue())
		except ValueError:
			wx.MessageBox("Invalid line entered.", "Error", wx.ICON_ERROR)
			self.Destroy()
			return
		if line <= self.frame.reader.GetNumberOfLines() and line > 0:
			pos = self.frame.reader.XYToPosition(0, line - 1)
			self.frame.reader.SetInsertionPoint(pos)
			self.Destroy()
		else:
			wx.MessageBox("Invalid line entered.", "Error", wx.ICON_ERROR)
			self.Destroy()

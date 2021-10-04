import wx
import sys
from documents.text import TextDocument
from . import dialogs
from repeating_timer import RepeatingTimer
from documents.pdf import PdfDocument
from documents.word import DocxDocument
from documents.epub import EpubDocument
from documents.markdown import MarkdownDocument
from documents.html import HtmlDocument
from documents.rtf import RtfDocument
import utils
from documents.powerpoint import PptxDocument

class MainFrame(wx.Frame):
	def __init__(self, app):
		self.app = app
		self.accel = []
		self.path = ""
		self.timer = RepeatingTimer(1.0, self.on_timer)
		wx.Frame.__init__(self, None, title=f"{self.app.name} V{self.app.version}", size=wx.DefaultSize)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.menu_bar = wx.MenuBar()
		self.file_menu = wx.Menu()
		self.m_open = self.file_menu.Append(wx.ID_ANY, "&Open (Control+O)")
		self.Bind(wx.EVT_MENU, self.on_open, self.m_open)
		self.file_menu.AppendSeparator()
		self.m_close = self.file_menu.Append(wx.ID_ANY, "E&xit")
		self.Bind(wx.EVT_MENU, self.on_close, self.m_close)
		self.menu_bar.Append(self.file_menu, "&File")
		self.tools_menu = wx.Menu()
		self.m_goto = self.tools_menu.Append(wx.ID_ANY, "&Goto... (Control+G)")
		self.Bind(wx.EVT_MENU, self.on_goto, self.m_goto)
		self.tools_menu.AppendSeparator()
		self.m_word_count = self.tools_menu.Append(wx.ID_ANY, "&Word Count (Control+W)")
		self.Bind(wx.EVT_MENU, self.on_word_count, self.m_word_count)
		self.menu_bar.Append(self.tools_menu, "&Tools")
		self.SetMenuBar(self.menu_bar)
		self.reader_t = wx.StaticText(parent=self.panel, pos=(0, 90))
		self.reader_t.SetLabel("&Text")
		self.main_box.Add(self.reader_t, 0, wx.ALL, 10)
		self.reader = wx.TextCtrl(parent=self.panel, pos=(0, 100), size=(1166, 768), style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_RICH2 | wx.TE_AUTO_URL | wx.TE_NOHIDESEL| wx.TE_DONTWRAP)
		self.main_box.Add(self.reader, 0, wx.ALL, 10)
		self.Bind(wx.EVT_CLOSE, self.on_close)
		self.accel.append((wx.ACCEL_CTRL, ord("O"), self.m_open.GetId()))
		self.accel.append((wx.ACCEL_CTRL, ord("G"), self.m_goto.GetId()))
		self.accel.append((wx.ACCEL_CTRL, ord("W"), self.m_word_count.GetId()))
		self.accel_table = wx.AcceleratorTable(self.accel)
		self.SetAcceleratorTable(self.accel_table)
		self.panel.Layout()
		self.timer.start()

	def on_close(self, event=None):
		self.Destroy()
		self.timer.stop()
		sys.exit()

	def on_open(self, event=None):
		dialog = wx.FileDialog(None, "Open", style=wx.FD_OPEN)
		if dialog.ShowModal() == wx.ID_OK:
			self.path = dialog.GetPath()
			if self.path.lower().endswith(".txt"):
				document = TextDocument(dialog.GetPath())
			elif self.path.lower().endswith(".txt"):
				document = TextDocument(dialog.GetPath())
			elif self.path.lower().endswith(".pdf"):
				document = PdfDocument(dialog.GetPath())
			elif self.path.lower().endswith(".docx"):
				document = DocxDocument(dialog.GetPath())
			elif self.path.lower().endswith(".epub"):
				document = EpubDocument(dialog.GetPath())
			elif self.path.lower().endswith(".md"):
				document = MarkdownDocument(dialog.GetPath())
			elif self.path.lower().endswith(".html") or self.path.lower().endswith(".htm"):
				document = HtmlDocument(dialog.GetPath())
			elif self.path.lower().endswith(".rtf"):
				document = RtfDocument(dialog.GetPath())
			elif self.path.lower().endswith(".pptx"):
				document = PptxDocument(dialog.GetPath())
			else:
				wx.MessageBox(f"{self.app.name} doesn't currently support this type of file.", "Error", wx.ICON_ERROR)
				return
			text = document.read()
			document.close()
			self.reader.SetValue(text)
			if self.path not in self.app.config.loaded_documents:
				self.app.config.loaded_documents[self.path] = 0
			self.reader.SetInsertionPoint(self.app.config.loaded_documents[self.path])

	def on_goto(self, event=None):
		dlg = dialogs.GotoDialog(self)
		dlg.Show()

	def on_timer(self):	
		if self.path != "":
			self.app.config.loaded_documents[self.path] = self.reader.GetInsertionPoint()

	def on_word_count(self, event=None):
		content = self.reader.GetValue()
		count = utils.count_words(content)
		wx.MessageBox(f"This document contains {count} {utils.plural(count, 'word', 'words')}", "Word count")

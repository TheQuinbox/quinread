import wx
import sys
from documents.text import TextDocument
from . import goto, preferences
from repeating_timer import RepeatingTimer
from documents.pdf import PdfDocument
from documents.word import DocxDocument
from documents.epub import EpubDocument
from documents.markdown import MarkdownDocument
from documents.html import HtmlDocument
from documents.rtf import RtfDocument
import utils
from documents.powerpoint import PptxDocument
from documents.mobi import MobiDocument
import updater
import threading
import os

class MainFrame(wx.Frame):
	def __init__(self, app):
		self.app = app
		self.accel = []
		self.filename = ""
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
		self.m_preferences = self.file_menu.Append(wx.ID_ANY, "&Preferences (Control+P)")
		self.Bind(wx.EVT_MENU, self.on_preferences, self.m_preferences)
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
		self.tools_menu.AppendSeparator()
		self.m_export_to_text = self.tools_menu.Append(wx.ID_ANY, "E&xport to text (Control+T)")
		self.Bind(wx.EVT_MENU, self.on_export_to_text, self.m_export_to_text)
		self.menu_bar.Append(self.tools_menu, "&Tools")
		self.help_menu = wx.Menu()
		self.m_about = self.help_menu.Append(wx.ID_ANY, "&About (F1)")
		self.Bind(wx.EVT_MENU, self.on_about, self.m_about)
		self.m_update = self.help_menu.Append(wx.ID_ANY, "Check for &updates (Control+u)")
		self.Bind(wx.EVT_MENU, self.on_update, self.m_update)
		self.menu_bar.Append(self.help_menu, "&Help")
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
		self.accel.append((wx.ACCEL_CTRL, ord("P"), self.m_preferences.GetId()))
		self.accel.append((wx.ACCEL_CTRL, ord("T"), self.m_export_to_text.GetId()))
		self.accel.append((wx.ACCEL_NORMAL, wx.WXK_F1, self.m_about.GetId()))
		self.accel.append((wx.ACCEL_CTRL, ord("u"), self.m_update.GetId()))
		self.accel_table = wx.AcceleratorTable(self.accel)
		self.SetAcceleratorTable(self.accel_table)
		self.reader.Enable(False)
		self.reader_t.Enable(False)
		self.panel.Layout()
		if self.app.config.last_loaded_path != "" and self.app.config.load_previous:
			text = self.load_file(self.app.config.last_loaded_path)
			if text == "":
				pass
			else:
				self.reader.SetValue(text)
				if self.path not in self.app.config.loaded_documents:
					self.app.config.loaded_documents[self.path] = 0
					self.app.config.last_loaded_path = self.path
				self.reader.SetInsertionPoint(self.app.config.loaded_documents[self.path])
				self.SetTitle(f"{self.filename} - {self.app.name} V{self.app.version}")
				self.reader.Enable(True)
		self.timer.start()

	def on_close(self, event=None):
		self.Destroy()
		self.timer.stop()
		sys.exit()

	def load_file(self, path):
		if not os.path.isfile(path):
			wx.MessageBox("That file doesn't exist", "Error", wx.ICON_ERROR)
			return ""
		if path.lower().endswith(".txt"):
			document = TextDocument(path)
		elif path.lower().endswith(".txt"):
			document = TextDocument(path)
		elif path.lower().endswith(".pdf"):
			document = PdfDocument(path)
		elif path.lower().endswith(".docx"):
			document = DocxDocument(path)
		elif path.lower().endswith(".epub"):
			document = EpubDocument(path)
		elif path.lower().endswith(".md"):
			document = MarkdownDocument(path)
		elif path.lower().endswith(".html") or self.path.lower().endswith(".htm"):
			document = HtmlDocument(path)
		elif path.lower().endswith(".rtf"):
			document = RtfDocument(path)
		elif path.lower().endswith(".pptx"):
			document = PptxDocument(path)
		elif path.lower().endswith(".mobi") or path.lower().endswith(".azw3"):
			document = MobiDocument(path)
		else:
			wx.MessageBox(f"{self.app.name} doesn't currently support this type of file.", "Error", wx.ICON_ERROR)
			return ""
		text = document.read()
		document.close()
		self.path = path
		self.filename = os.path.basename(self.path)
		self.SetTitle(f"{self.filename} - {self.app.name} V{self.app.version}")
		return text

	def on_open(self, event=None):
		dialog = wx.FileDialog(None, "Open", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_OK:
			self.path = dialog.GetPath()
			text = self.load_file(self.path)
			if text == "":
				return
			self.reader.SetValue(text)
			self.reader.Enable(True)
			self.reader.SetFocus()
			if self.path not in self.app.config.loaded_documents:
				self.app.config.loaded_documents[self.path] = 0
			self.app.config.last_loaded_path = self.path
			self.reader.SetInsertionPoint(self.app.config.loaded_documents[self.path])

	def on_goto(self, event=None):
		dlg = goto.GotoDialog(self)
		dlg.Show()

	def on_timer(self):	
		if self.path != "":
			self.app.config.loaded_documents[self.path] = self.reader.GetInsertionPoint()

	def on_word_count(self, event=None):
		content = self.reader.GetValue()
		count = utils.count_words(content)
		wx.MessageBox(f"This document contains {count} {utils.plural(count, 'word', 'words')}", "Word count")

	def on_preferences(self, event=None):
		dlg = preferences.PreferencesDialog(self.app)
		dlg.Show()

	def on_export_to_text(self, event=None):
		dialog = wx.FileDialog(None, "Save as", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, defaultFile=f"{self.filename}.txt")
		if self.reader.GetValue() == "" or self.path == "":
			wx.MessageBox("No document is currently loaded.", "Error", wx.ICON_ERROR)
			return
		if dialog.ShowModal() == wx.ID_OK:
			path = dialog.GetPath()
			f = open(path, "w")
			f.write(self.reader.GetValue())
			f.close()
		dialog.Destroy()

	def on_about(self, event=None):
		wx.MessageBox(f"{self.app.name} is copyright (c) 2021 by Quin Marilyn and other contributors. The {self.app.name} source code is licensed under the MIT license.", "About")

	def on_update(self, event=None):
		threading.Thread(target=updater.update_check, args=[self.app, False]).start()

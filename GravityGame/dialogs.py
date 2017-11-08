import wx
import wx.lib.buttons as buttons
#try:
#	from agw import pycollapsiblepane as PCP
#except ImportError: # if it's not there locally, try the wxPython lib.
#	import wx.lib.agw.pycollapsiblepane as PCP
import re
import os
import commands

class SplashScreen(wx.SplashScreen):
	def __init__(self, parent=None):
		# This is a recipe to a the screen.
		# Modify the following variables as necessary.
		aBitmap = wx.Image('images/titlescreen.png', wx.BITMAP_TYPE_PNG).Scale(1440,900).ConvertToBitmap()
		splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_NO_TIMEOUT
		splashDuration = 100000 # milliseconds
		# Call the constructor with the above arguments in exactly the
		# following order.
		wx.SplashScreen.__init__(self, aBitmap, splashStyle, splashDuration, parent)
		self.Bind(wx.EVT_CLOSE, self.OnExit)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnExit)

		wx.Yield()

	def OnExit(self, evt):
		self.Hide()
		os.system('mplayer -fs -input conf=/path/to/input.conf -vo gl:backend=4:glfinish titlevid.mpg')
		#self.Destroy()
		# The program will freeze without this line.
		evt.Skip()

class CameraSplashScreen(wx.SplashScreen):
	def __init__(self, parent=None):
		# This is a recipe to a the screen.
		# Modify the following variables as necessary.
		aBitmap = wx.Image('images/camtitlescreen.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_NO_TIMEOUT
		splashDuration = 1000000 # milliseconds
		# Call the constructor with the above arguments in exactly the
		# following order.
		wx.SplashScreen.__init__(self, aBitmap, splashStyle, splashDuration, parent)
		self.Bind(wx.EVT_CLOSE, self.OnExit)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnExit)

		wx.Yield()

	def OnExit(self, evt):
		self.Hide()
		# The program will freeze without this line.
		evt.Skip()

class FullScreen(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size = wx.Size(800,600))
		#self.ShowFullScreen(not self.IsFullScreen())

		self.panel = wx.Panel(self)
		self.SetBackgroundColour('black')

		#self.Bind(wx.EVT_CLOSE, self.OnExit)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnExit)

	def OnExit(self, evt):
		self.Close()

class HelpDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size = (650,250))

        vbox = wx.BoxSizer(wx.VERTICAL)

        message = '''\n 	Help astronomers at the IoA figure out how to de-lens these images!\n
	1) Pick a mass for your dark matter halo.
	2) Pick a distance between the dark matter halo and the Earth.
	3) Choose where to put your dark matter halo on the image.
	4) Click the "De-lens the galaxy!" button when you're done, and see if you guessed right!\n
	If you help de-lens all 10 images, you can try lensing a picture of your own face!'''
        stline2 = wx.StaticText(self, -1, style=wx.ALIGN_LEFT|wx.TOP)
        stline2.SetLabel(message)
        font2 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        stline2.SetFont(font2)
        vbox.Add(stline2, 1, wx.EXPAND)

        sizer =  self.CreateButtonSizer(wx.OK)
        vbox.Add(sizer, 0, wx.ALIGN_CENTER)

        self.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=1)
        self.Centre()
        self.Show()

    def OnOK(self, event):
        self.Close()

class CorrectDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (710,275))

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = '\nYou did it! Ready for the next image?'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		image = wx.StaticBitmap(self, -1, wx.Image('images/youdidit.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())

		vbox.Add(image, 1, wx.EXPAND)
		vbox.Add(stline2, 1, wx.EXPAND)
		#vbox.Add(hbox, 1, wx.EXPAND)

		sizer =  self.CreateButtonSizer(wx.OK)
		vbox.Add(sizer, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)
		self.Bind(wx.EVT_BUTTON, self.OnOK, id=1)
		self.Centre()
		self.Show()

	def OnOK(self, event):
		self.Close()

class IncorrectDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (720,275))

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = '\nNot quite... Try again?'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		image = wx.StaticBitmap(self, -1, wx.Image('images/tryagain.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())

		vbox.Add(image, 1, wx.EXPAND)
		vbox.Add(stline2, 1, wx.EXPAND)
		#vbox.Add(hbox, 1, wx.EXPAND)

		sizer =  self.CreateButtonSizer(wx.OK)
		vbox.Add(sizer, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)
		self.Bind(wx.EVT_BUTTON, self.OnOK, id=1)
		self.Centre()
		self.Show()

	def OnOK(self, event):
		self.Close()

class ThanksDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (635,320))

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = '\nEnjoy the rest of the exhibits here at the IoA!\nHave a good day, and may the science be with you!'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		image = wx.StaticBitmap(self, -1, wx.Image('images/thanks.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())

		vbox.Add(image, 1, wx.EXPAND)
		vbox.Add(stline2, 1, wx.EXPAND)
		#vbox.Add(hbox, 1, wx.EXPAND)

		sizer =  self.CreateButtonSizer(wx.OK)
		vbox.Add(sizer, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)
		self.Bind(wx.EVT_BUTTON, self.OnOK, id=1)
		self.Centre()
		self.Show()

	def OnOK(self, event):
		self.Close()

class WonGameDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (690,375))
		self.SetAffirmativeId(wx.ID_YES)
		self.SetEscapeId(wx.ID_NO)

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = '\nGood job! You de-lensed all the images!\nDo you want to try to lens a picture of yourself?'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		image = wx.StaticBitmap(self, -1, wx.Image('images/goodjob.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())

		vbox.Add(image, 1, wx.EXPAND)
		vbox.Add(stline2, 1, wx.EXPAND)

		btnsizer = wx.StdDialogButtonSizer()

		btn = wx.Button(self, wx.ID_YES)
		btn.SetDefault()
		btnsizer.AddButton(btn)

		btn = wx.Button(self, wx.ID_NO)
		btnsizer.AddButton(btn)
		btnsizer.Realize()

		#sizer =  self.CreateButtonSizer(wx.YES_NO)
		vbox.Add(btnsizer, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)

		self.Centre()
		self.Show()

class RaiseHandDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (550,400))

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = '\nGreat! Please raise your hand so a volunteer can take you to the Lens Your Face station!'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		image = wx.Image('images/handup.png', wx.BITMAP_TYPE_PNG)
		#image = image.Scale(268,268)
		image = wx.StaticBitmap(self, -1, image.ConvertToBitmap())

		vbox.Add(image, 1, wx.EXPAND)
		vbox.Add(stline2, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		#vbox.Add(hbox, 1, wx.EXPAND)

		sizer =  self.CreateButtonSizer(wx.OK)
		vbox.Add(sizer, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)
		self.Bind(wx.EVT_BUTTON, self.OnOK, id=1)
		self.Centre()
		self.Show()

	def OnOK(self, event):
		self.Close()

class IncorrectLocDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (720,275))

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = '\nNot quite... You\'ve put the halo in the wrong place. Try again?'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		image = wx.StaticBitmap(self, -1, wx.Image('images/tryagain.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())

		vbox.Add(image, 1, wx.EXPAND)
		vbox.Add(stline2, 1, wx.EXPAND)
		#vbox.Add(hbox, 1, wx.EXPAND)

		sizer =  self.CreateButtonSizer(wx.OK)
		vbox.Add(sizer, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)
		self.Bind(wx.EVT_BUTTON, self.OnOK, id=1)
		self.Centre()
		self.Show()

	def OnOK(self, event):
		self.Close()

class IncorrectMassDistDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (720,300))

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = '\nNot quite... This is what happens when you try to de-lens an image with a halo that\'s not the right mass or distance. Try again?'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		image = wx.StaticBitmap(self, -1, wx.Image('images/tryagain.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())

		vbox.Add(image, 1, wx.EXPAND)
		vbox.Add(stline2, 1, wx.EXPAND)
		#vbox.Add(hbox, 1, wx.EXPAND)

		sizer =  self.CreateButtonSizer(wx.OK)
		vbox.Add(sizer, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)
		self.Bind(wx.EVT_BUTTON, self.OnOK, id=1)
		self.Centre()
		self.Show()

	def OnOK(self, event):
		self.Close()

class DeadDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (755,275))

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = '\nOh no, you\'ve run out of lives!\nBetter luck next time!'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		image = wx.StaticBitmap(self, -1, wx.Image('images/dead.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())

		vbox.Add(image, 1, wx.EXPAND)
		vbox.Add(stline2, 1, wx.EXPAND)
		#vbox.Add(hbox, 1, wx.EXPAND)

		sizer =  self.CreateButtonSizer(wx.OK)
		vbox.Add(sizer, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)
		self.Bind(wx.EVT_BUTTON, self.OnOK, id=1)
		self.Centre()
		self.Show()

	def OnOK(self, event):
		self.Close()

'''
class SendLensedPicture(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (409,337))
		#self.mainPanel = wx.Panel(self)
		self.SetAffirmativeId(wx.ID_YES)
		self.SetEscapeId(wx.ID_NO)

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = 'Nice picture!\nDo you want to email it to yourself, or print it?'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		vbox.Add(stline2, 1, wx.EXPAND)

		hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.cpStyle = wx.CP_NO_TLW_RESIZE
		self.cp = cp = PCP.PyCollapsiblePane(self, style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
		#self.cp.SetButton(emailbtn)
		self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, cp)
		self.MakePaneContent(cp.GetPane())

		printimg = wx.Image('images/printer.png', wx.BITMAP_TYPE_PNG).Scale(100,100)
		printbtn = buttons.GenBitmapButton(self, wx.ID_NO, printimg.ConvertToBitmap())

		emailimg = wx.Image('images/email.png', wx.BITMAP_TYPE_PNG).Scale(100,100)
		emailbtn = buttons.GenBitmapButton(self.cp, wx.ID_YES, emailimg.ConvertToBitmap())
		self.cp.SetButton(emailbtn)

		#vbox.Add(emailbtn, 1, wx.EXPAND)
		vbox.Add(printbtn, 1, wx.ALIGN_LEFT)

		#sizer =  self.CreateButtonSizer(wx.YES_NO)
		vbox.Add(hbox, 0, wx.ALIGN_CENTER)

		vbox.Add(self.cp, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 25)
		self.SetSizer(vbox)
		self.Layout()

		self.Centre()
		self.Show()

	def OnPaneChanged(self, event=None):
		# redo the layout
		self.Layout()
		#print self.Size

	def MakePaneContent(self, pane):

		nameLbl = wx.StaticText(pane, -1, "Email:")
		name = wx.TextCtrl(pane, -1, "")

		addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
		addrSizer.AddGrowableCol(1)
		addrSizer.Add(nameLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
		addrSizer.Add(name, 0, wx.EXPAND)

		border = wx.BoxSizer(wx.VERTICAL)
		border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 5)

		btn = wx.Button(pane, -1, 'Send me the picture!')
		border.Add(btn, 1, wx.ALIGN_CENTER)
		pane.SetSizer(border)
'''

class PatienceScreen(wx.SplashScreen):
	def __init__(self, parent=None):
		# This is a recipe to a the screen.
		# Modify the following variables as necessary.
		aBitmap = wx.Image('images/patience3.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_NO_TIMEOUT
		splashDuration = 100000 # milliseconds
		# Call the constructor with the above arguments in exactly the
		# following order.
		wx.SplashScreen.__init__(self, aBitmap, splashStyle, splashDuration, parent)

		wx.Yield()

'''
class PatienceDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (550,400))

		vbox = wx.BoxSizer(wx.VERTICAL)

		message = '\nThis will take a minute or two.\nWhile you\'re waiting, why don\'t you ask the volunteers about some of the science behind this game?'
		stline2 = wx.StaticText(self, -1, style=wx.ALIGN_CENTER)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		image = wx.Image('images/patience2.jpg', wx.BITMAP_TYPE_ANY)
		#image = image.Scale(268,268)
		image = wx.StaticBitmap(self, -1, image.ConvertToBitmap())

		vbox.Add(image, 1, wx.EXPAND)
		vbox.Add(stline2, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
		#vbox.Add(hbox, 1, wx.EXPAND)

		sizer =  self.CreateButtonSizer(wx.OK)
		vbox.Add(sizer, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)
		self.Bind(wx.EVT_BUTTON, self.OnOK, id=1)
		self.Centre()
		self.Show()

	def OnOK(self, event):
		self.Close()
'''

class EmailPicture(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (500,225))

		panel = wx.Panel(self)
		border = wx.BoxSizer(wx.VERTICAL)

		message = 'Do you want to email your picture to yourself?\n'
		stline2 = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline2.SetLabel(message)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline2.SetFont(font2)

		border.Add(stline2, 0, wx.EXPAND)

		nameLbl = wx.StaticText(panel, -1, "Email:")
		self.name = wx.TextCtrl(panel, -1, "")

		addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=0)
		addrSizer.AddGrowableCol(1)
		addrSizer.Add(nameLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
		addrSizer.Add(self.name, 0, wx.EXPAND)

		border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 5)

		msg = '(You need to type a valid email address here.\nDon\'t worry, we won\'t store your email address.)\n'
		stline = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline.SetLabel(msg)
		font = wx.Font(15, wx.SWISS, wx.SLANT, wx.NORMAL)
		stline.SetFont(font)
		border.Add(stline, 0, wx.EXPAND)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.btn = wx.Button(panel, wx.ID_OK, 'Send me the picture!')
		self.btn.Enable(False)
		hbox.Add(self.btn, 0, wx.EXPAND)

		nobtn = wx.Button(panel, wx.ID_CANCEL, 'No thanks.')
		nobtn.Enable(True)
		hbox.Add(nobtn, 0, wx.EXPAND)

		border.Add(hbox, 1, wx.ALIGN_CENTER)
		panel.SetSizer(border)

		self.Bind(wx.EVT_TEXT, self.CheckEmail)

		self.Centre()
		self.Show()

	def CheckEmail(self, event):
		email = self.name.GetValue()
		if re.match("[^@]+@[^@]+\.[^@]+", email):
			self.email = email
			self.btn.Enable(True)
		
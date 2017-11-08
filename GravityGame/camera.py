import cv2
import wx
import do_lens_new as do_lens
import dialogs

class MyFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size = wx.Size(600,600))

		self.timer = wx.Timer(self, id=22)

		vboxtotal = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(vboxtotal)
		vboxtotal.Layout()

		#Create statusbar (just for testing)
		#self.statusbar = self.CreateStatusBar()

		#Toolbar
		self.toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL)
		#self.toolbar.AddSimpleTool(1, wx.Image('images/quit.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Close', '')
		self.toolbar.AddSimpleTool(2, wx.Image('images/extra_images/takepicture.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Take a picture', '')
		self.toolbar.AddSimpleTool(3, wx.Image('images/extra_images/lenspicture.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Lens the picture!', '')
		self.toolbar.EnableTool(3, False)
		self.toolbar.Realize()
		vboxtotal.Add(self.toolbar, 0, wx.EXPAND, border=5)

		#self.Bind(wx.EVT_TOOL, self.OnQuit, id=1)
		self.Bind(wx.EVT_TOOL, self.TakePic, id=2)
		self.Bind(wx.EVT_TOOL, self.OnLens, id=3)

		self.vidFrame = ShowCapture(self,capture)
		vboxtotal.Add(self.vidFrame, 1, wx.EXPAND)

		#self.Bind(wx.EVT_CLOSE, self.OnClose)

		self.Centre()
		self.Show()

		MySplash = dialogs.CameraSplashScreen()
		MySplash.Show()

	#def OnQuit(self, event):
		#self.Close()

	def TakePic(self, event):
		#self.statusbar.SetStatusText('Taking picture')
		self.vidFrame.CaptureImage()

		self.Bind(wx.EVT_TIMER, self.TookPic, self.timer)
		self.timer.Start(1000)

	def TookPic(self, event):
		dlg = wx.MessageDialog(self, 'Do you want to take another picture?','', wx.YES_NO | wx.NO_DEFAULT)
		result = dlg.ShowModal()
		dlg.Destroy()

		if result == wx.ID_YES:
			self.vidFrame.StartVideo()
		else:
			self.toolbar.EnableTool(2, False)
			self.toolbar.EnableTool(3, True)

		self.timer.Stop()
		test = self.Unbind(wx.EVT_TIMER, self.timer)

	def OnLens(self, event):
		'''
		dlg = wx.MessageDialog(self, 'Is this picture okay?','', wx.YES_NO | wx.NO_DEFAULT)
		result = dlg.ShowModal()
		dlg.Destroy()

		if result == wx.ID_NO:
			self.toolbar.EnableTool(2,True)
			self.toolbar.EnableTool(3,False)
			self.vidFrame.StartVideo()
		else:
		'''
		ask = dialogs.EmailPicture(self,-1,'')
		sendresult = ask.ShowModal()
		ask.Destroy()
		if sendresult == wx.ID_OK:
			to_email = ask.email
		else:
			to_email = ''

		#self.statusbar.SetStatusText('Lensing')
		patience = dialogs.PatienceScreen()
		patience.Show()
		do_lens.grav_lens("images/test_image.jpg","images/test_image_lensed.jpg")
		patience.Hide()

		#self.Bind(wx.EVT_TIMER, self.vidFrame.ShowLensedImage, self.timer)
		#self.timer.Start(1000)
		self.vidFrame.ShowLensedImage()

		if to_email != '':
			from testemail import SendEmail
			SendEmail(to_email)

		#thanks = dialogs.ThanksDialog(self,-1,'')
		#result = thanks.ShowModal()
		#thanks.Destroy()

		self.Bind(wx.EVT_TIMER, self.Finished, self.timer)
		self.timer.Start(1000)

	def Finished(self, event):
		#print 'made it here'
		thanks = dialogs.ThanksDialog(self,-1,'')
		result = thanks.ShowModal()
		thanks.Destroy()

		self.timer.Stop()
		test = self.Unbind(wx.EVT_TIMER, self.timer)

		MySplash = dialogs.CameraSplashScreen()
		MySplash.Show()

		self.toolbar.EnableTool(2,True)
		self.toolbar.EnableTool(3,False)
		self.vidFrame.StartVideo()

class ShowCapture(wx.Panel):
	def __init__(self, parent, capture):
		wx.Panel.__init__(self, parent)

		self.capture = capture
		self.fps = 15
		ret, frame = self.capture.read()
		frame=cv2.flip(frame,1)
		frame=frame[:,280:1000]

		height, width = frame.shape[:2]
		print height, width
		parent.SetSize((width, height))
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		self.bmp = wx.BitmapFromBuffer(width, height, frame)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_TIMER, self.NextFrame)

		self.StartVideo()

	def StartVideo(self):
		self.timer = wx.Timer(self)
		self.timer.Start(1000./self.fps)

	def OnPaint(self, evt):
		dc = wx.BufferedPaintDC(self)
		dc.DrawBitmap(self.bmp, 0, 0)

	def NextFrame(self, event):
		ret, frame = self.capture.read()
		if ret:
			frame=cv2.flip(frame,1)
			frame=frame[:,280:1000]
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			self.bmp.CopyFromBuffer(frame)
			self.Refresh()

	def CaptureImage(self):
		ret, frame = self.capture.read()
		if ret:
			#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			frame=cv2.flip(frame,1)
			frame=frame[:,280:1000]
			file = "images/test_image.jpg"
			cv2.imwrite(file, frame)
		self.timer.Stop()

		self.img = wx.Image("images/test_image.jpg", wx.BITMAP_TYPE_ANY)
		self.bmp = self.img.ConvertToBitmap()
		self.Refresh()

	def ShowLensedImage(self):
		#print 'showing image'
		#self.timer.Stop()

		self.img = wx.Image("images/test_image_lensed.jpg", wx.BITMAP_TYPE_ANY)
		W, H = self.Size
		newimage = self.img.Scale(W,H)
		self.bmp = newimage.ConvertToBitmap()
		self.Refresh()

capture = cv2.VideoCapture(0)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1280)

class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, -1, 'Lens your face!')
		return True

app = MyApp(0)
app.MainLoop()

capture.release()
cv2.destroyAllWindows()

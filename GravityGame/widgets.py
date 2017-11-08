#import os, sys
import wx
import numpy as np
import wx.lib.scrolledpanel as scrolled
from wx.lib.buttons import GenBitmapToggleButton
from wx.lib.buttons import GenButtonEvent
from wx.lib.pubsub import pub

class MassWidget(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1, style=wx.SIMPLE_BORDER)
		#self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
		#self.SetBackgroundColour('White')

		#Initialize mass
		self.Mass = 0

		vbox = wx.BoxSizer(wx.VERTICAL)

		masstitle = wx.StaticText(self, -1, "\nDark Matter Halo Mass\n", style=wx.ALIGN_CENTER)
		masstitle.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD))
		vbox.Add(masstitle, 0, wx.ALIGN_CENTER)

		hbox = wx.BoxSizer(wx.HORIZONTAL)

		vboxsmall = wx.BoxSizer(wx.VERTICAL)
		self.smallimg = wx.BitmapFromImage(wx.Image('images/bighalo.png', wx.BITMAP_TYPE_ANY).Scale(100,100))
		self.small = GenBitmapToggleButton(self, id = 1, bitmap = self.smallimg)
		vboxsmall.Add(self.small, 0, wx.EXPAND)
		textsmall = wx.StaticText(self, -1, "Light\n(500 billion\nSun masses)", style=wx.ALIGN_CENTRE_HORIZONTAL)
		textsmall.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
		vboxsmall.Add(textsmall, 0, wx.ALIGN_CENTER)
		hbox.Add(vboxsmall, 0, wx.ALIGN_CENTER)

		hbox.AddSpacer(30)

		'''
		vboxmed = wx.BoxSizer(wx.VERTICAL)
		self.medimg = wx.BitmapFromImage(wx.Image('images/medhalo.jpg', wx.BITMAP_TYPE_ANY))
		self.med = GenBitmapToggleButton(self, id = 2, bitmap = self.medimg)
		vboxmed.Add(self.med, 0, wx.EXPAND)
		textmed = wx.StaticText(self, -1, "Medium\n(15 Sun masses)", style=wx.ALIGN_CENTRE_HORIZONTAL)
		textmed.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
		vboxmed.Add(textmed, 0, wx.ALIGN_CENTER)
		hbox.Add(vboxmed, 0, wx.ALIGN_CENTER)

		hbox.AddSpacer(10)
		'''

		vboxbig = wx.BoxSizer(wx.VERTICAL)
		self.bigimg = wx.BitmapFromImage(wx.Image('images/bighalo.png', wx.BITMAP_TYPE_ANY).Scale(200,200))
		self.big = GenBitmapToggleButton(self, id = 3, bitmap = self.bigimg)
		vboxbig.Add(self.big, 0, wx.EXPAND)
		textbig = wx.StaticText(self, -1, "Heavy\n(2,000 billion\nSun masses)", style=wx.ALIGN_CENTRE_HORIZONTAL)
		textbig.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
		vboxbig.Add(textbig, 0, wx.ALIGN_CENTER)
		hbox.Add(vboxbig, 0, wx.ALIGN_CENTER)

		vbox.Add(hbox, 0, wx.ALIGN_CENTER)

		caption = wx.StaticText(self, -1, "\nChoose how massive the halo is!", style=wx.ALIGN_CENTER)
		caption.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
		vbox.Add(caption, 0, wx.ALIGN_CENTER)

		self.Bind(wx.EVT_BUTTON, self.OnSmallClick, id=1)
		#self.Bind(wx.EVT_BUTTON, self.OnMedClick, id=2)
		self.Bind(wx.EVT_BUTTON, self.OnBigClick, id=3)

		self.SetSizer(vbox)

	def OnSmallClick(self, event):
		if self.Mass == 0:
			self.Mass = 1
		elif self.Mass == 1:
			self.Mass = 0
		else:
			#self.med.SetToggle(False)
			self.big.SetToggle(False)
			self.Mass = 1

		pub.sendMessage('mass.update', message = self.Mass)

	'''
	def OnMedClick(self, event):
		if self.Mass == 0:
			self.Mass = 15
		elif self.Mass == 15:
			self.Mass = 0
		else:
			self.small.SetToggle(False)
			self.big.SetToggle(False)
			self.Mass = 15

		pub.sendMessage('mass.update', message = self.Mass)
	'''

	def OnBigClick(self, event):
		if self.Mass == 0:
			self.Mass = 2
		elif self.Mass == 2:
			self.Mass = 0
		else:
			self.small.SetToggle(False)
			#self.med.SetToggle(False)
			self.Mass = 2

		pub.sendMessage('mass.update', message = self.Mass)

	def NewRound(self):
		self.Mass = 0
		self.small.SetToggle(False)
		#self.med.SetToggle(False)
		self.big.SetToggle(False)

		pub.sendMessage('mass.update', message = self.Mass)

class DistanceWidget(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1, style=wx.SIMPLE_BORDER)
		#self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
		#self.SetBackgroundColour('White')

		#initialize distance
		self.Distance = '1'

		vbox = wx.BoxSizer(wx.VERTICAL)

		disttitle = wx.StaticText(self, -1, "\nDark Matter Halo Distance\n", style=wx.ALIGN_CENTER)
		disttitle.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD))
		vbox.Add(disttitle, 0, wx.ALIGN_CENTER)

		panel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
		firstimage = wx.Image('images/near.png', wx.BITMAP_TYPE_ANY).Scale(516,178)
		self.picture = wx.StaticBitmap(panel, wx.ID_ANY, wx.BitmapFromImage(firstimage))
		vbox.Add(panel, 0, wx.ALIGN_CENTER)

		msg = '(Image NOT to scale.)\n'
		stline = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.TOP)
		stline.SetLabel(msg)
		font = wx.Font(15, wx.SWISS, wx.SLANT, wx.NORMAL)
		stline.SetFont(font)
		vbox.Add(stline, 0, wx.ALIGN_CENTER)

		self.images = [wx.Image('images/near.png', wx.BITMAP_TYPE_ANY).Scale(516,178), wx.Image('images/far.png', wx.BITMAP_TYPE_ANY).Scale(516,178)]
		self.dists = ['1','2'] #['near', 'med', 'far']
		distlabels = ['Near Earth (15 million light-years)','Far from Earth (50 million light-years)'] #['Near', 'Med', 'Far']

		self.rb = wx.RadioBox(self, -1, "", wx.DefaultPosition, wx.DefaultSize, distlabels, 2, wx.RA_SPECIFY_COLS | wx.NO_BORDER)
		self.Bind(wx.EVT_RADIOBOX, self.OnSelect)
		vbox.Add(self.rb, 0,wx.ALIGN_CENTER)

		caption = wx.StaticText(self, -1, "\nChoose how far the halo is from the Earth!\n", style=wx.ALIGN_CENTER)
		caption.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL))
		vbox.Add(caption, 0, wx.ALIGN_CENTER)

		self.SetSizer(vbox)

	def OnSelect(self, event):
		item = event.GetSelection()
		self.Distance = self.dists[item]
		self.picture.SetFocus()
		self.picture.SetBitmap(wx.BitmapFromImage(self.images[item]))
		pub.sendMessage('dist.update', message = self.Distance)

	def NewRound(self):
		self.rb.SetSelection(0)
		self.Distance = self.dists[0]
		self.picture.SetFocus()
		self.picture.SetBitmap(wx.BitmapFromImage(self.images[0]))
		pub.sendMessage('dist.update', message = self.Distance)

class ImagePanel(wx.Panel):
	def __init__(self, parent):
		super(ImagePanel, self).__init__(parent)

		pub.subscribe(self.UpdateImage, 'image.update')

		self._grid = 3

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_MOUSE_EVENTS, self.InWindow)
		self.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveWindow)
		self.Bind(wx.EVT_LEFT_DOWN, self.ChooseRect)

		self.Location = -1
		self.rect = np.zeros(self._grid*self._grid)
		self.finalrect = np.zeros(self._grid*self._grid)

	def UpdateImage(self, message):
		self.image = 'images/' + message + '.jpg'
		self.img = wx.Image(self.image, wx.BITMAP_TYPE_ANY)
		self.bmp = self.img.ConvertToBitmap()

		#resize the new image
		W, H = self.Size
		if W > H:
			NewW = W
			NewH = W * H / W
		else:
			NewH = H
			NewW = H * W / H
		newimage = self.img.Scale(NewW,NewH)
		self.bmp = newimage.ConvertToBitmap()

		self.Refresh()

	def OnSize(self, evt):
		# Redraw as we are resized
		W, H = self.Size
		#oldW, oldH = self.bmp.Size
		#print oldW, oldH
		if W > H:
			NewW = W
			NewH = W * H / W
		else:
			NewH = H
			NewW = H * W / H
		newimage = self.img.Scale(NewW,NewH)
		self.bmp = newimage.ConvertToBitmap()
		#print(NewW)
		#print(NewH)
		self.Refresh()
		evt.Skip()

	def SetGrid(self, grid):
		self._grid = grid
		self.Refresh() # Repaint

	def OnPaint(self, evt):
		dc = wx.PaintDC(self)
		
		# Draw image
		dc.DrawBitmap(self.bmp,0,0)

		# Draw mouseover rectangles
		dc.SetBrush(wx.TRANSPARENT_BRUSH)
		dc.SetPen(wx.Pen(wx.YELLOW, 3, wx.DOT_DASH))

		rect = self.GetClientRect()
		rectX = rect.Width / self._grid
		rectY = rect.Height / self._grid

		if self.rect[0] == True:
			dc.DrawRectangle(0,0,rectX, rectY)
		elif self.rect[1] == True:
			dc.DrawRectangle(rectX,0,rectX, rectY)
		elif self.rect[2] == True:
			dc.DrawRectangle(rectX*2,0,rectX, rectY)
		elif self.rect[3] == True:
			dc.DrawRectangle(0,rectY,rectX, rectY)
		elif self.rect[4] == True:
			dc.DrawRectangle(rectX,rectY,rectX, rectY)
		elif self.rect[5] == True:
			dc.DrawRectangle(rectX*2,rectY,rectX, rectY)
		elif self.rect[6] == True:
			dc.DrawRectangle(0,rectY*2,rectX, rectY)
		elif self.rect[7] == True:
			dc.DrawRectangle(rectX,rectY*2,rectX, rectY)
		elif self.rect[8] == True:
			dc.DrawRectangle(rectX*2,rectY*2,rectX, rectY)

		# Draw selection rectangle
		dc.SetPen(wx.Pen(wx.RED, 3, wx.SOLID))

		if self.finalrect[0] == True:
			dc.DrawRectangle(0,0,rectX, rectY)
		elif self.finalrect[1] == True:
			dc.DrawRectangle(rectX,0,rectX, rectY)
		elif self.finalrect[2] == True:
			dc.DrawRectangle(rectX*2,0,rectX, rectY)
		elif self.finalrect[3] == True:
			dc.DrawRectangle(0,rectY,rectX, rectY)
		elif self.finalrect[4] == True:
			dc.DrawRectangle(rectX,rectY,rectX, rectY)
		elif self.finalrect[5] == True:
			dc.DrawRectangle(rectX*2,rectY,rectX, rectY)
		elif self.finalrect[6] == True:
			dc.DrawRectangle(0,rectY*2,rectX, rectY)
		elif self.finalrect[7] == True:
			dc.DrawRectangle(rectX,rectY*2,rectX, rectY)
		elif self.finalrect[8] == True:
			dc.DrawRectangle(rectX*2,rectY*2,rectX, rectY)

	def InWindow(self, evt):
		panel_pos = self.ScreenToClient(wx.GetMousePosition())
		rect = self.GetClientRect()
		rectx = rect.Width / self._grid
		recty = rect.Height / self._grid
		if (panel_pos[1] < recty):
			if (panel_pos[0] < rectx):
				self.rect = self.rect*0
				self.rect[0] = True
			elif (rectx < panel_pos[0]) and (panel_pos[0] < rectx*2):
				self.rect = self.rect*0
				self.rect[1] = True
			elif (rectx*2 < panel_pos[0]):
				self.rect = self.rect*0
				self.rect[2] = True
		elif (recty < panel_pos[1]) and (panel_pos[1] < recty*2):
			if (panel_pos[0] < rectx):
				self.rect = self.rect*0
				self.rect[3] = True
			elif (rectx < panel_pos[0]) and (panel_pos[0] < rectx*2):
				self.rect = self.rect*0
				self.rect[4] = True
			elif (rectx*2 < panel_pos[0]):
				self.rect = self.rect*0
				self.rect[5] = True
		else:
			if (panel_pos[0] < rectx):
				self.rect = self.rect*0
				self.rect[6] = True
			elif (rectx < panel_pos[0]) and (panel_pos[0] < rectx*2):
				self.rect = self.rect*0
				self.rect[7] = True
			elif (rectx*2 < panel_pos[0]):
				self.rect = self.rect*0
				self.rect[8] = True

		self.Refresh()

	def LeaveWindow(self, evt):
		self.rect = self.rect*0
		self.Refresh()

	def ChooseRect(self, evt):
		panel_pos = self.ScreenToClient(wx.GetMousePosition())
		rect = self.GetClientRect()
		rectx = rect.Width / self._grid
		recty = rect.Height / self._grid
		if (panel_pos[1] < recty):
			if (panel_pos[0] < rectx):
				self.finalrect = self.finalrect*0
				self.finalrect[0] = True
				self.Location = 1
			elif (rectx < panel_pos[0]) and (panel_pos[0] < rectx*2):
				self.finalrect = self.finalrect*0
				self.finalrect[1] = True
				self.Location = 2
			elif (rectx*2 < panel_pos[0]):
				self.finalrect = self.finalrect*0
				self.finalrect[2] = True
				self.Location = 3
		elif (recty < panel_pos[1]) and (panel_pos[1] < recty*2):
			if (panel_pos[0] < rectx):
				self.finalrect = self.finalrect*0
				self.finalrect[3] = True
				self.Location = 4
			elif (rectx < panel_pos[0]) and (panel_pos[0] < rectx*2):
				self.finalrect = self.finalrect*0
				self.finalrect[4] = True
				self.Location = 5
			elif (rectx*2 < panel_pos[0]):
				self.finalrect = self.finalrect*0
				self.finalrect[5] = True
				self.Location = 6
		else:
			if (panel_pos[0] < rectx):
				self.finalrect = self.finalrect*0
				self.finalrect[6] = True
				self.Location = 7
			elif (rectx < panel_pos[0]) and (panel_pos[0] < rectx*2):
				self.finalrect = self.finalrect*0
				self.finalrect[7] = True
				self.Location = 8
			elif (rectx*2 < panel_pos[0]):
				self.finalrect = self.finalrect*0
				self.finalrect[8] = True
				self.Location = 9

		self.Refresh()
		pub.sendMessage('loc.update', message = self.Location)

	def NewRound(self):
		self.rect = self.rect*0
		self.finalrect = self.finalrect*0
		self.Refresh()
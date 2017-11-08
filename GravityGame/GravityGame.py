#!/usr/local/bin/python

# GravityGame.py

#import os, sys
import wx
import numpy as np
import wx.lib.scrolledpanel as scrolled
from wx.lib.buttons import GenBitmapToggleButton
from wx.lib.buttons import GenButtonEvent
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import random
import dialogs
import time
import widgets

class MyFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size = wx.Size(800,600))

		self.timer = wx.Timer(self, id=22)

		self.ShowFullScreen(not self.IsFullScreen())
		MySplash = dialogs.SplashScreen() #(None, -1, '')
		MySplash.Show()

		##########################
		#Define some key variables
		##########################
		#Round number
		self.n = 0
		#Total number of rounds
		self.nRounds = 4
		#Total number of lives
		self.nLives = 10
		self.nLivesleft = self.nLives
		#List of images to choose from
		self.imagelist	= np.genfromtxt('images/listlensedimages.csv', delimiter=',', dtype='str', usecols=0) #['galaxy','galaxy','galaxy','galaxy','galaxy']
		self.distlist	= np.genfromtxt('images/listlensedimages.csv', delimiter=',', dtype='str', usecols=2) #['near','near','near']
		self.masslist	= np.genfromtxt('images/listlensedimages.csv', delimiter=',', dtype='str', usecols=3) #[10,10,10]
		self.loclist	= np.genfromtxt('images/listlensedimages.csv', delimiter=',', dtype='str', usecols=1) #[4,4,4]

		#Create statusbar (just for testing)
		#self.statusbar = self.CreateStatusBar()

		#Main sizer
		vboxtotal = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(vboxtotal)
		vboxtotal.Layout()

		########
		#Toolbar
		########
		self.toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL)
		self.toolbar.AddSimpleTool(1, wx.Image('images/newgame.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'New', '')
		self.toolbar.AddSimpleTool(2, wx.Image('images/help.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Help', '')
		#self.toolbar.AddSimpleTool(3, wx.Image('images/quit.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Quit', '')
		self.toolbar.AddSimpleTool(4, wx.Image('images/lens3.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'De-lens!', '')
		self.toolbar.Realize()
		self.toolbar.EnableTool(4, False)
		toolbox = wx.BoxSizer(wx.HORIZONTAL)
		toolbox.Add(self.toolbar, 0, wx.EXPAND, border=5)

		toolbox.Add([50,100])

		msg2 = 'Round '+str(self.n+1)+'/'+str(self.nRounds)
		self.roundLabel = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.ALIGN_BOTTOM)
		self.roundLabel.SetLabel(msg2)
		font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.roundLabel.SetFont(font)
		toolbox.Add(self.roundLabel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=5)

		toolbox.Add([50,100])

		#Lives counter
		msg = 'Lives left:'
		stline = wx.StaticText(self, -1, style=wx.ALIGN_CENTER|wx.ALIGN_BOTTOM)
		stline.SetLabel(msg)
		font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL)
		stline.SetFont(font)
		toolbox.Add(stline, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=5)

		toolbox.Add([10,100])

		self.lives = []
		for i in range(self.nLives):
			life = wx.StaticBitmap(self, -1, wx.Image('images/goldstar.png', wx.BITMAP_TYPE_PNG).Scale(50,50).ConvertToBitmap())
			self.lives.append(life)
			toolbox.Add(life, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border=5)

		vboxtotal.Add(toolbox, 0, wx.EXPAND)

		self.Bind(wx.EVT_TOOL, self.OnNew, id=1)
		self.Bind(wx.EVT_TOOL, self.OnHelp, id=2)
		#self.Bind(wx.EVT_TOOL, self.OnQuit, id=3)
		self.Bind(wx.EVT_TOOL, self.OnLens, id=4)

		#Set up sizer for the rest of the widgets
		grid = wx.FlexGridSizer(1,2,5,5)

        #Parameter widgets
		vboxleft = wx.BoxSizer(wx.VERTICAL)

		####################
		#DM halo mass widget
		####################
		self.pnl1 = widgets.MassWidget(self)
		self.mass = self.pnl1.Mass
		vboxleft.Add(self.pnl1, 1, wx.EXPAND) 

		########################
		#DM halo distance widget
		########################
		self.pnl2 = widgets.DistanceWidget(self)
		self.dist = self.pnl2.Distance
		vboxleft.Add(self.pnl2, 1, wx.EXPAND) 

		##########################
		#Image and location widget
		##########################
		self.MyImage = widgets.ImagePanel(self)
		#Choose image from imagelist, and remove it from imagelist (so it doesn't come up again in a later round)
		imagenum = np.random.choice(len(self.imagelist))
		self.Image = self.imagelist[imagenum]
		np.delete(self.imagelist,imagenum)

		#Choose masses, distances, locations that correspond with image choice, and remove from lists
		self.correctMass = self.masslist[imagenum]
		self.correctDist = self.distlist[imagenum]
		self.correctLoc = self.loclist[imagenum]
		np.delete(self.masslist,imagenum)
		np.delete(self.distlist,imagenum)
		np.delete(self.loclist,imagenum)

		#Send ImagePanel the file to open
		msg = 'lensed/' + str(self.Image) + '_' + str(self.correctLoc) + str(self.correctDist) + str(self.correctMass) + '_len'
		pub.sendMessage('image.update', message = msg)
		self.loc = 0

		#print msg

		grid.AddMany([(vboxleft, 1, wx.EXPAND | wx.ALL), (self.MyImage, 1, wx.EXPAND | wx.ALL, 3)])
		grid.AddGrowableCol(1)
		grid.AddGrowableRow(0)

		vboxtotal.Add(grid, 1, wx.EXPAND)

		#Get updates from widgets on where the user has picked mass/distance/location
		pub.subscribe(self.OnMassUpdate, 'mass.update')
		pub.subscribe(self.OnDistUpdate, 'dist.update')
		pub.subscribe(self.OnLocUpdate, 'loc.update')

		self.Show()

	def OnMassUpdate(self, message):
		self.mass = message
		#self.statusbar.SetStatusText(str(self.loc)+','+str(self.dist)+','+str(self.mass))
		if (self.mass > 0) and (self.loc >= 1) and (self.dist > 0):
			self.toolbar.EnableTool(4, True)
		else:
			self.toolbar.EnableTool(4, False)

	def OnDistUpdate(self, message):
		self.dist = message
		#self.statusbar.SetStatusText(str(self.loc)+','+str(self.dist)+','+str(self.mass))
		if (self.mass > 0) and (self.loc >= 1) and (self.dist > 0):
			self.toolbar.EnableTool(4, True)
		else:
			self.toolbar.EnableTool(4, False)

	def OnLocUpdate(self, message):
		self.loc = message
		#self.statusbar.SetStatusText(str(self.loc)+','+str(self.dist)+','+str(self.mass))
		#print self.loc, self.correctLoc
		if (self.mass > 0) and (self.loc >= 1) and (self.dist > 0):
			self.toolbar.EnableTool(4, True)
		else:
			self.toolbar.EnableTool(4, False)

	def OnNew(self, event):
		#self.statusbar.SetStatusText('New Command')
		self.NewGame()

	def OnHelp(self, event):
		helpmessage = dialogs.HelpDialog(self, -1, 'How to Play')
		val = helpmessage.ShowModal()
		helpmessage.Destroy()

	def OnQuit(self, event):
		self.Close()

	def OnLens(self, event):
		#self.statusbar.SetStatusText('De-lensing')

		#put these back in later
		#msg = str(self.Image) + '_' + str(self.mass) + str(self.dist) + str(self.loc)
		#pub.sendMessage('image.update', message = msg)

		#If location isn't right, don't update image - just tell them they're wrong
		if (str(self.loc) != str(self.correctLoc)): 
			#Remove a life
			self.nLivesleft = self.nLivesleft - 1
			self.lives[self.nLivesleft].Hide()

			#Check how many lives are left
			if self.nLivesleft == 0:
				self.Dead()
			else:
				incorrectmessage = dialogs.IncorrectLocDialog(self,-1,'')
				val = incorrectmessage.ShowModal()
				incorrectmessage.Destroy()

		else:
			#If everything is correct, show correct dialog and start a new round
			if (str(self.mass) == str(self.correctMass)) and (str(self.dist) == str(self.correctDist)): 
				msg = 'delensed/' + str(self.Image) + '_' + str(self.correctLoc) + str(self.correctDist) + str(self.correctMass) + '_' + str(self.correctLoc) + str(self.correctDist) + str(self.correctMass)
				pub.sendMessage('image.update', message = msg)

				self.Bind(wx.EVT_TIMER, self.CorrectChoice, self.timer)
				self.timer.Start(1000)

			#If something else is wrong, update image and tell them they're wrong
			else:
				msg = 'delensed/' + str(self.Image) + '_' + str(self.correctLoc) + str(self.correctDist) + str(self.correctMass) + '_' + str(self.loc) + str(self.dist) + str(self.mass)
				pub.sendMessage('image.update', message = msg)

				self.Bind(wx.EVT_TIMER, self.WrongChoice, self.timer)
				self.timer.Start(1000)

	def CorrectChoice(self, event):
		correctmessage = dialogs.CorrectDialog(self,-1,'')
		val = correctmessage.ShowModal()
		correctmessage.Destroy()

		self.timer.Stop()
		test = self.Unbind(wx.EVT_TIMER, self.timer)

		self.n += 1
		self.NewRound()

	def WrongChoice(self, event):
		#Remove a life
		self.nLivesleft = self.nLivesleft - 1
		self.lives[self.nLivesleft].Hide()

		self.timer.Stop()
		test = self.Unbind(wx.EVT_TIMER, self.timer)

		#Check how many lives are left
		if self.nLivesleft == 0:
			self.Dead()

		else:
			incorrectmessage = dialogs.IncorrectMassDistDialog(self,-1,'')
			val = incorrectmessage.ShowModal()
			incorrectmessage.Destroy()

		#Then show the old image again
		msg = 'lensed/' + str(self.Image) + '_' + str(self.correctLoc) + str(self.correctDist) + str(self.correctMass) + '_len'
		#self.loc = 0
		self.toolbar.EnableTool(4, False)
		#self.MyImage.NewRound()
		pub.sendMessage('image.update', message = msg)

	def NewRound(self):
		#Refresh mass and distance widgets for new round
		self.pnl1.NewRound()
		self.pnl2.NewRound()

		#Disable lens button
		self.loc = 0
		self.toolbar.EnableTool(4, False)

		#Check round number
		###################
		#self.statusbar.SetStatusText(str(self.n))
		if self.n >= self.nRounds:
			dlg = dialogs.WonGameDialog(self,1,'') #wx.MessageDialog(self, 'Good job! You de-lensed all the images!\nDo you want to try to lens a picture of yourself?','', wx.YES_NO | wx.YES_DEFAULT)
			result = dlg.ShowModal()
			dlg.Destroy()
			if result == wx.ID_YES:
				#self.statusbar.SetStatusText('Yay!')
				dlg = dialogs.RaiseHandDialog(self, -1, '') #wx.MessageDialog(self, 'Great! Raise your hand and ask one of the volunteers to let you try the Lens Your Face station!','') #,wx.ICON_EXCLAMATION)
				dlg.ShowModal()
				dlg.Destroy()
				self.NewGame()
			else:
				thanks = dialogs.ThanksDialog(self, -1, '')
				result = thanks.ShowModal()
				thanks.Destroy()
				self.NewGame()

		#Set a new image
		################
		else:
			#Update round number
			msg2 = 'Round '+str(self.n+1)+'/'+str(self.nRounds)
			self.roundLabel.SetLabel(msg2)

			#Choose image from imagelist, and remove it from imagelist (so it doesn't come up again in a later round)
			imagenum = np.random.choice(len(self.imagelist))
			self.Image = self.imagelist[imagenum]
			np.delete(self.imagelist,imagenum)

			#Choose masses, distances, locations that correspond with image choice, and remove from lists
			self.correctMass = self.masslist[imagenum]
			self.correctDist = self.distlist[imagenum]
			self.correctLoc = self.loclist[imagenum]
			np.delete(self.masslist,imagenum)
			np.delete(self.distlist,imagenum)
			np.delete(self.loclist,imagenum)

			#Send ImagePanel the file to open
			msg = 'lensed/' + str(self.Image) + '_' + str(self.correctLoc) + str(self.correctDist) + str(self.correctMass) + '_len'
			#print msg
			self.MyImage.NewRound()
			pub.sendMessage('image.update', message = msg)

	def Dead(self):
		msg = dialogs.DeadDialog(self, -1, 'Game Over')
		val = msg.ShowModal()
		msg.Destroy()	

		self.NewGame()	

	def NewGame(self):
		#List of images to choose from
		self.imagelist	= np.genfromtxt('images/listlensedimages.csv', delimiter=',', dtype='str', usecols=0) #['galaxy','galaxy','galaxy','galaxy','galaxy']
		self.distlist	= np.genfromtxt('images/listlensedimages.csv', delimiter=',', dtype='str', usecols=2) #['near','near','near']
		self.masslist	= np.genfromtxt('images/listlensedimages.csv', delimiter=',', dtype='str', usecols=3) #[10,10,10]
		self.loclist	= np.genfromtxt('images/listlensedimages.csv', delimiter=',', dtype='str', usecols=1) #[4,4,4]

		#Reset number of rounds
		self.n = 0
		#Reset number of lives and show all lives
		self.nLivesleft = self.nLives
		for i in range(self.nLivesleft):
			self.lives[i].Show()

		MySplash = dialogs.SplashScreen()
		MySplash.Show()
		self.NewRound()

class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, -1, 'Gravity Game')
		#frame.Show(True)
		frame.Centre()
		return True

app = MyApp(0)
app.MainLoop()
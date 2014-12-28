#!/usr/bin/python

import sys
import parsemanifest
import appwindow
import httplib
import json
import os
import thread
import shutil
from PyQt4 import QtGui as qtgui
from PyQt4 import QtCore

class LoginWindow(qtgui.QWidget):
	def __init__(self):
		self.loginUrl = 'localhost:3000'
		self.conn = httplib.HTTPConnection(self.loginUrl)
		self.headers = {"Content-type":"application/json"}
		super(LoginWindow, self).__init__()
		hbox = qtgui.QHBoxLayout()
		hbox1 = qtgui.QHBoxLayout()

		lableuser = qtgui.QLabel()
		lableuser.setText("User:      ")
		lablepwd  = qtgui.QLabel()
		lablepwd.setText("Password:")

		self.inputUser = qtgui.QLineEdit()
		self.inputpwd = qtgui.QLineEdit()

		vbox = qtgui.QVBoxLayout()

		hbox.addWidget(lableuser)
		hbox.addWidget(self.inputUser)

		hbox1.addWidget(lablepwd)
		hbox1.addWidget(self.inputpwd)

		self.loginBtn = qtgui.QPushButton()
		self.loginBtn.setText("Login")

		vbox.addLayout(hbox)
		vbox.addLayout(hbox1)
		vbox.addWidget(self.loginBtn)

		self.setLayout(vbox)
		self.setWindowTitle("User Login")
		self.connect(self.loginBtn, QtCore.SIGNAL("clicked()"), self.doLogin)
		self.loginFlag = False
		
	def doLogin(self):
		username = self.inputUser.text()
		userpwd = self.inputpwd.text()
		params = ({"account":str(username), "password":str(userpwd)})
		postdata = json.JSONEncoder().encode(params)
		self.conn.request("POST" ,"/users/login" ,postdata, self.headers)
		res = self.conn.getresponse()
		print res.status
		data = res.read()
		self.conn.close()
		if (res.status == 200):
			mainDir = os.path.dirname(os.path.abspath(__file__))
			mainwin = appwindow.AppMainWindow(mainDir)
			self.loginFlag = True
			self.close()
			mainwin.exec_()

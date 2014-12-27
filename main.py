#!/usr/bin/python

from PyQt4 import QtGui as qtgui
import sys
import appwindow
import loginwindow

app = qtgui.QApplication(sys.argv)
w = loginwindow.LoginWindow()
w.show()

if w.loginFlag:
	print "haha"

sys.exit(app.exec_())


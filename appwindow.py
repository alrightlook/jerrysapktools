#!/usr/bin/python

import sys
import parsemanifest
import os
import thread
import shutil
from PyQt4 import QtGui as qtgui
from PyQt4 import QtCore

class AppMainWindow(qtgui.QDialog):
	def __init__(self, targetFolder):
		super(AppMainWindow, self).__init__()
		self.openfilebtn = qtgui.QPushButton()
		self.openfilebtn.setText("Open An APK File")
		self.vbox = qtgui.QVBoxLayout()

		hbox = qtgui.QHBoxLayout()
		packagelable = qtgui.QLabel()
		packagelable.setText("PackageName:")
		self.packageNameEditor = qtgui.QLineEdit()
		hbox.addWidget(packagelable)
		hbox.addWidget(self.packageNameEditor)
		self.vbox.addLayout(hbox)

		self.infoLabel = qtgui.QLabel()
		self.infoLabel.setFixedHeight(100)
		self.infoLabel.setFixedWidth(35)

		hbox2 = qtgui.QHBoxLayout() 
		self.buildbtn = qtgui.QPushButton()
		self.buildbtn.setText("Build")
		hbox2.addWidget(self.buildbtn)

		hbox3 = qtgui.QHBoxLayout()
		vbox3 = qtgui.QVBoxLayout()

		self.previewIcon = qtgui.QLabel()
		self.previewIcon.setFixedWidth(512)
		self.previewIcon.setFixedHeight(512)

		self.chooseIcon = qtgui.QPushButton()
		self.chooseIcon.setText("Choose Icon")

		self.chooseCornor = qtgui.QPushButton()
		self.chooseCornor.setText("Choose Cornor")

		self.saveIcon = qtgui.QPushButton()
		self.saveIcon.setText("Save Icon")

		vbox3.addWidget(self.infoLabel)
		vbox3.addWidget(self.chooseIcon)
		vbox3.addWidget(self.chooseCornor)
		vbox3.addWidget(self.saveIcon)
		hbox3.addLayout(vbox3)
		hbox3.addWidget(self.previewIcon)

		hbox2.addWidget(self.openfilebtn)
		self.vbox.addLayout(hbox2)
		self.fileName = ""
		self.vbox.addLayout(hbox3)
		self.setLayout(self.vbox)
		self.connect(self.openfilebtn, QtCore.SIGNAL("clicked()"), self.openFile)
		self.connect(self.buildbtn, QtCore.SIGNAL("clicked()"), self.buildApk)
		self.connect(self.chooseIcon, QtCore.SIGNAL("clicked()"), self.doChooseIcon)
		self.connect(self.chooseCornor, QtCore.SIGNAL("clicked()"), self.doChooseCorner)
		self.connect(self.saveIcon, QtCore.SIGNAL("clicked()"), self.doSaveIcon)
		self.setWindowTitle("Jerry's Apk Tools")
		self.setGeometry(100,100,300,300)
		self.currentPath = targetFolder #os.path.dirname(os.path.abspath(__file__))
		self.unpackFolder = targetFolder + "/decompile"
		if not os.path.exists(self.unpackFolder):
			    os.makedirs(self.unpackFolder)

	def doSaveIcon(self):
		self.apkIconPath = self.manifest.getIconPath()
		tempApkIconPath = self.apkIconPath.replace("@drawable/", self.foldername + "/res/drawable/")
		print tempApkIconPath
		self.iconPixmap.save(tempApkIconPath + ".png", "PNG")

		tempApkIconPath = self.apkIconPath.replace("@drawable/", self.foldername + "/res/drawable-hdpi/")
		self.iconPixmap.save(tempApkIconPath + ".png", "PNG")
		
		tempApkIconPath = self.apkIconPath.replace("@drawable/", self.foldername + "/res/drawable-ldpi/")
		self.iconPixmap.save(tempApkIconPath + ".png", "PNG")
		
		tempApkIconPath = self.apkIconPath.replace("@drawable/", self.foldername + "/res/drawable-mdpi/")
		self.iconPixmap.save(tempApkIconPath + ".png", "PNG")
		
		tempApkIconPath = self.apkIconPath.replace("@drawable/", self.foldername + "/res/drawable-xhdpi/")
		self.iconPixmap.save(tempApkIconPath + ".png", "PNG")
		
		tempApkIconPath = self.apkIconPath.replace("@drawable/", self.foldername + "/res/drawable-xxhdpi/")
		self.iconPixmap.save(tempApkIconPath + ".png", "PNG")
		
	def doChooseCorner(self):
		
		chooseCornerDialog = qtgui.QFileDialog()
		if( chooseCornerDialog.exec_()):
			self.cornerName = chooseCornerDialog.getOpenFileName(self, "Choose Corner", "", "apk files(*.apk)")
			self.cornerFile = self.cornerName[0]
			cornerPixmap = qtgui.QPixmap(str(self.cornerFile))
			print "the corner file is:" + self.cornerFile
			painter = qtgui.QPainter(self.iconPixmap)
			painter.setCompositionMode(qtgui.QPainter.CompositionMode_Source);
			painter.drawPixmap(0,0, self.iconPixmap)
			painter.setCompositionMode(qtgui.QPainter.CompositionMode_SourceOver)
			painter.drawPixmap(0,0, cornerPixmap)
			painter.end()
			self.previewIcon.setPixmap(self.iconPixmap)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()
	def closeEvent(self, event):
		shutil.rmtree(self.unpackFolder)
	def buildDone(self):
		print "Build Ok"

	def buildApk(self):
		newApkFileName = qtgui.QFileDialog().getSaveFileName()
		print "saved file is:" + newApkFileName
		inputPackage = self.packageNameEditor.text()
		if( inputPackage != ""):
			self.manifest.setPackageName(inputPackage)
			self.manifest.save()
		cmd = "apktool b %s %s"%(self.foldername, os.path.basename(self.foldername) + ".apk")
		cmd = cmd.replace("(", "\(")
		cmd = cmd.replace(")", "\)")
		print "the cmd is :" + cmd
		thread.start_new_thread(self.doCommand, (cmd, self.buildDone))

	def doChooseIcon(self):
		chooseIconDialog = qtgui.QFileDialog()
		if( chooseIconDialog.exec_()):
			self.iconName = chooseIconDialog.selectedFiles()
			self.iconFileName = self.iconName[0]
			pixmap = qtgui.QPixmap(str(self.iconFileName))
			self.iconPixmap = pixmap
			print "The icon is:" + self.iconFileName
			self.previewIcon.setPixmap(pixmap)

	def openFile(self):
		self.openFileDialog = qtgui.QFileDialog()
		self.openFileDialog.setNameFilter("ApkFiles(*.apk)")
		if (self.openFileDialog.exec_()):
			self.fileName = self.openFileDialog.selectedFiles()
		if(self.fileName != ""):
			self.unPackFile()
	def done(self):
		self.androidManifestPath = self.foldername + "/Androidmanifest.xml"
		self.manifest = parsemanifest.ParseManifest(self.androidManifestPath)
		packageName = self.manifest.getPackageName()
		self.packageNameEditor.setText(packageName)
		

	def unPackFile(self):
		if(self.fileName != ""):
			self.foldername = self.unpackFolder + "/" + os.path.basename(str(self.fileName[0]))[:-4]
			cmd = "apktool d  -f %s %s"%(self.fileName[0], self.foldername)
			cmd = cmd.replace("(", "\(")
			cmd = cmd.replace(")", "\)")
			print 'The unPack Command is %s'%cmd

			thread.start_new_thread(self.doCommand, (cmd,self.done))

	def doCommand(self, cmd, cb):
		result = os.popen(cmd).read()
		cb()


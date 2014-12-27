#!/usr/bin/python

import sys
import os
import thread
import shutil
from PyQt4 import QtGui as qtgui
from PyQt4 import QtCore

import xml.etree.ElementTree as ET;

class ParseManifest:
	def __init__(self, path):
		self.path = path
		self.ns = "{http://schemas.android.com/apk/res/android}"
		ET.register_namespace("android", "http://schemas.android.com/apk/res/android");       ## register for android namespace
		self.tree = ET.parse(self.path);
		self.root = self.tree.getroot();
		self.applicationNode = self.root.find('application');
		self.packageName = self.root.attrib['package']
		for activity in self.applicationNode:
			activtiyname = activity.attrib
			print activtiyname[self.ns+'name']

	def getIconPath(self):
		icon = self.applicationNode.attrib[self.ns+'icon']
		print icon
		return icon
		
	def getPackageName(self):
		print self.packageName
		return self.packageName

	def setPackageName(self, packagename):
		self.packageName = packagename
		self.root.set('package', str(packagename))
	def save(self):
		self.tree.write(self.path)

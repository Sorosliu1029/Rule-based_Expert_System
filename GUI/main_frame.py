#!/usr/bin/python
# encoding:utf-8
# -*- Mode: Python -*-
# Author: Soros Liu <soros.liu1029@gmail.com>

# ==================================================================================================
# Copyright 2016 by Soros Liu
#
#                                                                          All Rights Reserved
"""

"""
import wx
import os
import re
import sys
sys.path.append('..')
from Picture_handler.cv_handler import PreHandler, FactGenerator
__author__ = 'Soros Liu'


class MainFrame(wx.Frame):
    """

    """
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title,
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX |
                                                          wx.MAXIMIZE_BOX))
        self.SetSize(size)
        self.Center()
        self.lineNumLabel = wx.StaticText(self, label='Line Number: ', pos=(10, 20), size=(40, 25))
        self.lineNumText = wx.TextCtrl(self, pos=(110, 20), size=(100, 20))
        self.shapeNumLabel = wx.StaticText(self, label='Shape Number: ', pos=(10, 50), size=(40, 25))
        self.shapeNumText = wx.TextCtrl(self, pos=(110, 50), size=(100, 20))
        self.openPicButton = wx.Button(self, label='Open File', pos=(880, 10), size=(100, 30))
        self.openPicButton.Bind(wx.EVT_BUTTON, self.open_picture)
        self.detectButton = wx.Button(self, label='Detect', pos=(880, 40), size=(100, 30))
        self.detectButton.Bind(wx.EVT_BUTTON, self.detect)
        self.pic_path = None
        self.title = title
        self.bmp = None
        self.Show()

    def open_picture(self, event):
        file_wildcard = 'picture file(*.png)|*.png|All files(*.*)|*.*'
        dlg = wx.FileDialog(self, 'Open Picture File', (os.getcwd() + '/../test'), style=wx.OPEN, wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.pic_path = dlg.GetPath()
            self.SetTitle(self.title + '--shape from ' + re.findall(r'test/(.*)$', dlg.GetPath())[0])
        else:
            dlg.Destroy()
            return
        dlg.Destroy()
        self.show_picture(self.pic_path, (10, 100))

    def show_picture(self, path, pos):
        pic = wx.Image(path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bmp = wx.StaticBitmap(self, 0, pic, pos=pos)
        bmp.Show()


    def detect(self, event):
        pass

if __name__ == '__main__':
    app = wx.App()
    MainFrame(None, -1, title='Shape Detector', size=(1000, 790))
    app.MainLoop()
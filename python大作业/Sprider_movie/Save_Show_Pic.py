# -*- coding: utf-8 -*-
#by KuroNeko
import base64

import os
import wx
from wx.lib.embeddedimage import PyEmbeddedImage


class ShowDataPic ( wx.Frame ):
    def __init__( self, parent ,openPath):#路径参数作为文件名可以直接区分不同的图，以达到重用该存储类
        wx.Frame.__init__ ( self, parent,title = openPath)
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        # openPath = self.GetDesktopPath()+"\\电影类别数据分析图.png"#在客户端函数中已经存储了一张图片，现在将结果写入
        file = open(openPath, 'rb')
        str = file.read()
        b64 = base64.b64encode(str)
        file.close()
        bitmap = PyEmbeddedImage(b64).GetBitmap()
        self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, bitmap )
        bSizer1.Add( self.m_bitmap1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )
        self.Centre( wx.BOTH )
    def GetDesktopPath(self):#再次定义桌面路径
        return os.path.join(os.path.expanduser("~"), 'Desktop')
if __name__=='__main__':
    app = wx.App()
    gui = ShowDataPic(None)
    gui.Show()
    app.MainLoop()
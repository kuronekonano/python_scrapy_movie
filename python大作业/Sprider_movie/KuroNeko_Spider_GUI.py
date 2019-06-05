# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
## by KuroNeko
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import pickle
import socket
import threading
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pymysql
import xlwt as ExcelWrite
from xlwt import Borders, XFStyle, Pattern
import wx
import wx.xrc
import os
lock_flag = threading.Lock()
###########################################################################
## Class SpiderClient
###########################################################################
import Save_Show_Pic
import KuroNeko_Spider_Server
class SpiderClient ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"KuroNeko-Spider_Client", pos = wx.DefaultPosition, size = wx.Size( 605,755 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        #主窗口
        self.toltime = 0

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour(wx.Colour(255, 255, 168))

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        fgSizer7 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer7.SetFlexibleDirection( wx.BOTH )
        fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.url_label = wx.StaticText( self, wx.ID_ANY, u"By KuroNeko", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )#地址栏标签
        self.url_label.Wrap( -1 )
        self.url_label.SetFont( wx.Font( 12, 70, 90, 90, False, "Tempus Sans ITC" ) )

        fgSizer7.Add( self.url_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.movie_url = wx.TextCtrl( self, wx.ID_ANY, u"豆瓣电影————https://movie.douban.com/", wx.DefaultPosition, wx.Size( 400,-1 ), wx.TE_READONLY )#地址栏文本框
        self.movie_url.SetBackgroundColour(wx.Colour(255, 255, 168))
        self.movie_url.SetFont(wx.Font(12, 70, 90, 90, False, "Tempus Sans ITC"))
        fgSizer7.Add( self.movie_url, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer5.Add( fgSizer7, 0, 0, 5 )

        fgSizer2 = wx.FlexGridSizer( 0, 8, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.type_label = wx.StaticText( self, wx.ID_ANY, u"类别:", wx.DefaultPosition, wx.DefaultSize, 0 )#类别标签
        self.type_label.Wrap( -1 )
        self.type_label.SetFont( wx.Font( 12, 70, 90, 90, False, "黑体" ) )

        fgSizer2.Add( self.type_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        #电影分类下拉框
        movie_typeChoices = [ u"热门", u"最新", u"经典", u"可播放", u"豆瓣高分", u"冷门佳片", u"华语", u"欧美", u"韩国",u"日本", u"动作", u"喜剧", u"爱情", u"科幻", u"悬疑", u"恐怖", u"动画" ]
        self.movie_type = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, movie_typeChoices, 0 )
        self.movie_type.SetSelection( 0 )
        self.movie_type.SetFont( wx.Font( 11, 70, 90, 90, False, "幼圆" ) )
        self.movie_type.SetBackgroundColour(wx.Colour(165, 253, 142))
        self.movie_type.SetForegroundColour(wx.Colour(243, 31, 222))

        fgSizer2.Add( self.movie_type, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.sort_way = wx.StaticText( self, wx.ID_ANY, u"排序:", wx.DefaultPosition, wx.DefaultSize, 0 )#排序方式标签
        self.sort_way.Wrap( -1 )
        self.sort_way.SetFont( wx.Font( 12, 70, 90, 90, False, "黑体" ) )

        fgSizer2.Add( self.sort_way, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        movie_sortChoices = [ u"热度", u"时间", u"评价" ]#排序方式下拉框
        self.movie_sort = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, movie_sortChoices, 0 )
        self.movie_sort.SetSelection( 0 )
        self.movie_sort.SetFont( wx.Font( 11, 70, 90, 90, False, "幼圆" ) )
        self.movie_sort.SetBackgroundColour(wx.Colour(255, 255, 168))
        self.movie_sort.SetForegroundColour(wx.Colour(243, 31, 222))

        fgSizer2.Add( self.movie_sort, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.thread_label = wx.StaticText( self, wx.ID_ANY, u"线程数:", wx.DefaultPosition, wx.DefaultSize, 0 )#线程数标签
        self.thread_label.Wrap( -1 )
        self.thread_label.SetFont( wx.Font( 12, 70, 90, 90, False, "黑体" ) )

        fgSizer2.Add( self.thread_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        threadNumChoices = [ u"1", u"2", u"3", u"4", u"5",u"6",u"7" ]#线程数量下拉框
        self.threadNum = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, threadNumChoices, 0 )
        self.threadNum.SetSelection( 2 )#初始化下拉选项
        self.threadNum.SetFont(wx.Font(13, 70, 90, 92, False, "幼圆"))
        self.threadNum.SetForegroundColour(wx.Colour(243, 31, 222))
        self.threadNum.SetBackgroundColour(wx.Colour(192, 243, 241))

        fgSizer2.Add( self.threadNum, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.page_label = wx.StaticText( self, wx.ID_ANY, u"页数:", wx.DefaultPosition, wx.DefaultSize, 0 )#页数标签
        self.page_label.Wrap( -1 )
        self.page_label.SetFont( wx.Font( 12, 70, 90, 90, False, "黑体" ) )

        fgSizer2.Add( self.page_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.pageNum = wx.TextCtrl( self, wx.ID_ANY, "1", wx.DefaultPosition, wx.Size( 35,-1 ), wx.TE_CENTRE )#输入页数文本框
        fgSizer2.Add( self.pageNum, 0, wx.ALL, 5 )


        bSizer5.Add( fgSizer2, 0, 0, 5 )

        fgSizer3 = wx.FlexGridSizer( 0, 5, 0, 0 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.get_way = wx.StaticText(self, wx.ID_ANY, u"执行方式：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.get_way.Wrap(-1)
        self.get_way.SetFont(wx.Font(12, 70, 90, 90, False, "黑体"))

        fgSizer3.Add(self.get_way, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        query_typeChoices = [u"快速爬虫", u"完整爬虫"]
        self.query_type = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, query_typeChoices, 0)
        self.query_type.SetSelection(0)
        self.query_type.SetFont(wx.Font(12, 70, 90, 90, False, "幼圆"))
        self.query_type.SetForegroundColour(wx.Colour(255, 0, 0))
        self.query_type.SetBackgroundColour(wx.Colour(228, 202, 255))

        fgSizer3.Add(self.query_type, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.start = wx.Button( self, wx.ID_ANY, u"开始爬虫✔", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )#启动爬虫按钮start
        self.start.SetFont( wx.Font( 12, 70, 90, 90, False, "幼圆" ) )
        self.start.SetBackgroundColour(wx.Colour(165, 253, 142))
        self.start.SetForegroundColour(wx.Colour(243, 31, 222))

        fgSizer3.Add( self.start, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.export = wx.Button( self, wx.ID_ANY, u"导出数据♋", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )#导出数据按钮export
        self.export.SetFont( wx.Font( 12, 70, 90, 90, False, "幼圆" ) )
        self.export.SetBackgroundColour(wx.Colour(183, 245, 253))
        self.export.SetForegroundColour(wx.Colour(243, 31, 222))

        fgSizer3.Add( self.export, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.analyze = wx.Button( self, wx.ID_ANY, u"数据分析图♐", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )#分析数据按钮analyze
        self.analyze.SetFont( wx.Font( 12, 70, 90, 90, False, "幼圆" ) )
        self.analyze.SetForegroundColour(wx.Colour(177, 37, 218))
        self.analyze.SetBackgroundColour(wx.Colour(255, 187, 119))

        fgSizer3.Add( self.analyze, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.analyze2 = wx.Button(self, wx.ID_ANY, u"线程散点图♌", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER)  # 分析数据按钮analyze
        self.analyze2.SetFont(wx.Font(12, 70, 90, 90, False, "幼圆"))
        self.analyze2.SetForegroundColour(wx.Colour(255, 0, 0))
        self.analyze2.SetBackgroundColour(wx.Colour(228, 202, 255))

        fgSizer3.Add(self.analyze2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.clear = wx.Button(self, wx.ID_ANY, u"✘清空✘", wx.DefaultPosition, wx.DefaultSize,
                                  wx.NO_BORDER)
        self.clear.SetFont(wx.Font(12, 70, 90, 90, False, "幼圆"))
        self.clear.SetForegroundColour(wx.Colour(255, 0, 0))
        self.clear.SetBackgroundColour(wx.Colour(255, 255, 168))
        fgSizer3.Add(self.clear, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)


        bSizer5.Add( fgSizer3, 0, 0, 5 )

        fgSizer4 = wx.FlexGridSizer( 0, 1, 0, 0 )
        fgSizer4.SetFlexibleDirection( wx.BOTH )
        fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.log_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 575,520 ), wx.TE_MULTILINE )
        fgSizer4.Add( self.log_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.log_text.SetFont(wx.Font(9, 75, 90, 90, False, "微软雅黑"))
        self.log_text.SetBackgroundColour(wx.Colour(211, 243, 203))

        bSizer5.Add( fgSizer4, 0, 0, 5 )

        self.m_staticText_select = wx.StaticText(self, wx.ID_ANY, u"选择内容:",(70,400), wx.DefaultSize, 0)  # 内容标签
        self.m_staticText_select.Wrap(-1)
        self.m_staticText_select.SetFont(wx.Font(12, 70, 90, 90, False, "黑体"))
        fgSizer2.Add(self.m_staticText_select, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.turn_off=wx.CheckBox(self,label="关灯",pos=(530,25))
        self.turn_off.SetFont(wx.Font(10, 70, 90, 90, False, "黑体"))
        self.turn_off.SetForegroundColour(wx.Colour(0,0,0))
        self.turn_off.Bind(wx.EVT_CHECKBOX,self.onChecked)#关灯事件监听

        self.movie_name_check = wx.CheckBox(self, label='电影名', pos=(100,75))
        self.movie_name_check.SetFont(wx.Font(10, 70, 90, 90, False, "黑体"))
        self.movie_name_check.SetForegroundColour(wx.Colour( 255, 0, 0 ))
        self.movie_comment_check = wx.CheckBox(self, label='评论', pos=(180,75))
        self.movie_comment_check.SetFont(wx.Font(10, 70, 90, 90, False, "黑体"))
        self.movie_comment_check.SetForegroundColour(wx.Colour( 255, 128, 0 ))
        self.movie_director_check = wx.CheckBox(self, label='导演', pos=(240,75))
        self.movie_director_check.SetFont(wx.Font(10, 70, 90, 90, False, "黑体"))
        self.movie_director_check.SetForegroundColour(wx.Colour( 6, 18, 249 ))
        self.movie_actor_check = wx.CheckBox(self, label='主演', pos=(310,75))
        self.movie_actor_check.SetFont(wx.Font(10, 70, 90, 90, False, "黑体"))
        self.movie_actor_check.SetForegroundColour(wx.Colour( 0, 128, 0 ))
        self.movie_discussion_check = wx.CheckBox(self, label='论坛讨论', pos=(390,75))
        self.movie_discussion_check.SetFont(wx.Font(10, 70, 90, 90, False, "黑体"))
        self.movie_discussion_check.SetForegroundColour(wx.Colour( 7, 170, 248 ))
        self.movie_anothername_check = wx.CheckBox(self, label='电影别名', pos=(480,75))
        self.movie_anothername_check.SetFont(wx.Font(10, 70, 90, 90, False, "黑体"))
        self.movie_anothername_check.SetForegroundColour(wx.Colour( 128, 0, 255 ))
        self.movie_name_check.SetValue(1)
        self.movie_comment_check.SetValue(1)
        self.movie_director_check.SetValue(1)
        self.movie_actor_check.SetValue(1)
        self.movie_discussion_check.SetValue(1)
        self.movie_anothername_check.SetValue(1)
        self.SetSizer( bSizer5 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.start.Bind( wx.EVT_BUTTON, self.startSpider )#点击触发事件，此处是调用类中开始爬虫函数事件
        self.export.Bind( wx.EVT_BUTTON, self.exportData )#导出事件监听
        self.analyze.Bind( wx.EVT_BUTTON, self.analyzeData )#电影数据分析监听
        self.analyze2.Bind( wx.EVT_BUTTON, self.analyzeData2 )#日志数据分析监听
        self.clear.Bind(wx.EVT_BUTTON,self.Clear_log)

        #movie_type [ u"热门", u"最新", u"经典", u"可播放", u"豆瓣高分", u"冷门佳片", u"华语", u"欧美", u"韩国",u"日本", u"动作", u"喜剧", u"爱情", u"科幻", u"悬疑", u"恐怖", u"动画" ]
        self.movie_type_list = [
                        '%E7%83%AD%E9%97%A8',
                        '%E6%9C%80%E6%96%B0',
                        '%E7%BB%8F%E5%85%B8',
                        '%E5%8F%AF%E6%92%AD%E6%94%BE',
                        '%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86',
                        '%E5%86%B7%E9%97%A8%E4%BD%B3%E7%89%87',
                        '%E5%8D%8E%E8%AF%AD',
                        '%E6%AC%A7%E7%BE%8E',
                        '%E9%9F%A9%E5%9B%BD',
                        '%E6%97%A5%E6%9C%AC',
                        '%E5%8A%A8%E4%BD%9C',
                        '%E5%96%9C%E5%89%A7',
                        '%E7%88%B1%E6%83%85',
                        '%E7%A7%91%E5%B9%BB',
                        '%E6%82%AC%E7%96%91',
                        '%E6%81%90%E6%80%96',
                        '%E5%8A%A8%E7%94%BB'
                        ]
        #movie_sort
        self.movie_sort_list = ['recommend','time','rank']
        self.log_text.SetForegroundColour(wx.Colour(24, 50, 226))
        self.log_text.AppendText('>>>>>>>>>>>>>>>>\n')
        self.log_text.AppendText('(๑°3°๑)小可爱正在满世界找服务器(｡>∀<｡)...\n')
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.s.connect(('localhost',12306))
            self.log_text.AppendText("\n找到辣辣辣辣get！٩( 'ω' )و ！！！！！！！\n")
            self.log_text.AppendText("<<<<<<<<<<<<<<<<\n")
        except:
            self.s = None
            print("error：没找到服务器，可能你没开")
            self.log_text.AppendText("\n（╯‵□′）╯︵┴─┴  ...\n")
            self.log_text.AppendText("┴─┴︵╰（‵□′╰）    ...\n")
            self.log_text.AppendText("竟然没找到!!!∑(°Д°ノ)ノ！！！等会儿再试试(ó﹏ò｡)\n")
            self.log_text.AppendText("<<<<<<<<<<<<<<<<\n")
            return
# ===============================================================================================================
    def __del__( self ):
        pass

    def Clear_log(self,e):
        self.log_text.Clear()
    def onChecked(self,e):
        flag=self.turn_off.GetValue()
        if flag:
            self.SetBackgroundColour(wx.Colour(64, 64, 64))
            self.log_text.SetBackgroundColour(wx.Colour(96, 96, 96))
            self.movie_url.SetBackgroundColour(wx.Colour(264, 64, 64))
        else:
            self.SetBackgroundColour(wx.Colour(255, 255, 168))
            self.log_text.SetBackgroundColour(wx.Colour(211, 243, 203))
            self.movie_url.SetBackgroundColour(wx.Colour(255, 255, 168))

    # Virtual event handlers, overide them in your derived class
    def startSpider( self, event ):#点击并开始爬虫，此事件仅仅是为开始爬虫做准备，包括爬虫要求的整理，服务器的链接校验，直到最后才调用了真正启动爬虫的线程
        page_info = []#用于收集要传送的到爬虫服务器的选择信息
        if self.pageNum.GetValue() == "":#若未能获取到爬取页数，显示错误提示
            wx.MessageBox('请输入页数',caption="错误提示")
            return
        if int(self.pageNum.GetValue()) <= 0:#若输入页数格式错误，显示错误提示
            wx.MessageBox('页数应该大于0',caption="错误提示")
            return
        if self.s == None:#若链接超时则重新链接
            self.log_text.AppendText('>>>>>>>>>>>>>>>>\n')
            self.log_text.AppendText('(๑°3°๑)小可爱又在满世界找服务器(｡>∀<｡)...\n')
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                self.s.connect(('localhost',12306))
                self.log_text.AppendText("\n找到辣辣辣辣get！٩( 'ω' )و ！！！！！！！\n")
                self.log_text.AppendText("<<<<<<<<<<<<<<<<\n")
            except:
                self.log_text.SetForegroundColour(wx.Colour(255, 0, 0))
                self.s = None
                print("error：没找到服务器，可能你没开")
                self.log_text.AppendText("\n（╯‵□′）╯︵┴─┴  ...\n")
                self.log_text.AppendText("┴─┴︵╰（‵□′╰）    ...\n")
                self.log_text.AppendText("竟然没找到!!!∑(°Д°ノ)ノ！！！快去检查服务器开没(ó﹏ò｡)\n")
                self.log_text.AppendText("<<<<<<<<<<<<<<<<\n")
                return
        movie_type = self.movie_type_list[self.movie_type.GetSelection()]#获取输入的电影标签
        movie_sort = self.movie_sort_list[self.movie_sort.GetSelection()]#获取输入的排序方式
        threadNum = self.threadNum.GetString(self.threadNum.GetSelection())#获取输入的线程数
        pageNum = self.pageNum.GetValue()#获取输入的页数
        query_type = self.query_type.GetSelection()#获取爬取方式
        print('标签:',movie_type)#标签
        print('排序方式：',movie_sort)#排序方式
        print('线程数：',threadNum)#线程数
        print('页数：',pageNum)#页数
        print('爬虫方式：',query_type)#采集方式
        # page_info[movie_type,movie_sort,threadNum,pageNum,query_type]
        page_info.append(movie_type)#全部打包到要发送的List中
        page_info.append(movie_sort)
        page_info.append(threadNum)
        page_info.append(pageNum)
        page_info.append(query_type)
        page_info.append(self.movie_name_check.GetValue())#复选框信息
        page_info.append(self.movie_director_check.GetValue())
        page_info.append(self.movie_actor_check.GetValue())
        page_info.append(self.movie_anothername_check.GetValue())
        page_info.append(self.movie_comment_check.GetValue())
        page_info.append(self.movie_discussion_check.GetValue())
        threading.Thread(target=self.showLog,args=(page_info,)).start()#开启新线程调用爬虫程序

    def showLog(self,page_info):#真正开始爬虫的函数
        try:
            starttime = datetime.datetime.now()#起始时间
            self.s.sendall(pickle.dumps(page_info))#转化为byte传输
            flag = 0#返回的线程计数
            num=0
            self.log_text.SetForegroundColour(wx.Colour(255, 128, 0))
            while True:
                recv_data=self.s.recv(10240).decode()#接收并转码
                print(recv_data)
                if recv_data == "end":
                    flag = flag+1#当一个线程返回end时表示线程结束，所有线程结束时退出循环
                    print(flag,page_info[2])
                    if flag == int(page_info[2]):
                        self.log_text.SetForegroundColour(wx.Colour(128, 0, 255))#结束爬取标志颜色
                        self.log_text.AppendText(recv_data)#在图形界面中显示结束标志
                        break
                    continue
                self.log_text.AppendText(recv_data)#在图形界面中显示电影信息
                num=num+1
            endtime = datetime.datetime.now()#结束时间
            self.toltime =  (endtime - starttime).seconds
            self.log_text.AppendText("\n运行耗时:"+str(self.toltime)+"s\n")

            Clientlog = open('spider_log.txt', 'ba+')
            Clientlog.write(str("\t*****爬虫日志*****\t\n").encode('utf-8'))
            Clientlog.write(str("[开始时间]"+str(starttime.strftime('%Y/%m/%d %H:%M:%S'))+'\n').encode('utf-8'))
            Clientlog.write(str("[结束时间]"+str(endtime.strftime('%Y/%m/%d %H:%M:%S'))+'\n').encode('utf-8'))
            Clientlog.write(str("[线程数]"+str(page_info[2])+'\n').encode('utf-8'))
            Clientlog.write(str("[爬取数据量]"+str(num)+'\n').encode('utf-8'));
            Clientlog.write(str("[总耗时]"+str((endtime - starttime).seconds)+'s\n').encode('utf-8'))
            conn = pymysql.connect(host='localhost',user='root',password='970922',db='mytest',port=3306,charset='utf8')
            cur = conn.cursor()
            sql = 'insert into data_log values(null ,"%s","%s","%s")' % (num,(endtime - starttime).seconds,page_info[2])
            cur.execute(sql)
            conn.commit()
        except:
            wx.MessageBox('采集启动失败！！！',caption="错误提示")
        self.s.close()#注意这个链接是爬完一次就直接关掉的，而不是被归到except下面，否则会直接导致第二次爬虫无限等待因为上一次爬虫仍然占用原端口
        self.s = None


    def exportData( self, event ):#导出数据库中电影信息
        savePath = self.GetDesktopPath()+"\\豆瓣电影信息.xls"
        threading.Thread(target=self.writeXls,args=(savePath,)).start()#线程写入Excel表格
    def analyzeData( self, event ):#分析数据，参数为调用 <统计电影类型数量> 的函数
        self.matplotlib_show(self.count_type())
    def analyzeData2(self, event ):#分析数据2,日志信息散点图
        self.matplotlib_show2()


    def writeXls(self ,file_name):#写入Excel表格
        movie_list = ['上映年份','片名','导演','编剧','主演','类型','制片国家地区','语言','又名','上映日期','片长','IMDB链接/影片地址','评分','评价人数','页面网址','短评','话题']
        xls = ExcelWrite.Workbook()
        sheet = xls.add_sheet("Sheet1")#写入表1
        style = XFStyle()
        pattern = Pattern()                 # 创建一个模式
        pattern.pattern = Pattern.SOLID_PATTERN     # 设置其模式为实型
        pattern.pattern_fore_colour = 0x16        #设置其模式单元格背景色
        # 设置单元格背景颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,  the list goes on...
        style.pattern = pattern
        for i in range(len(movie_list)):#写入首行信息，为表头，表示列名
            sheet.write(0,i,movie_list[i],style)
            sheet.col(i).width = 5240

        actors_list=['姓名','性别','星座','年龄','出生地','职业','简介']
        sheet2=xls.add_sheet("Sheet2")
        style2 = XFStyle()
        style2.pattern = pattern
        for i in range(len(actors_list)):  # 写入首行信息，为表头，表示列名
            sheet2.write(0, i, actors_list[i], style2)
            sheet2.col(i).width = 5140
        try:
            #连接数据库读取数据
            conn = pymysql.connect(host='localhost',user='root',password='970922',db='mytest',port=3306,charset='utf8')
            cur = conn.cursor()
            sql = 'select * from movies'
            cur.execute(sql)
            row = 0
            for movie_info in cur.fetchall():#遍历数据库中每行信息，一行表示一部电影的所有信息
                row = row+1#第0行为表头，不添加数据，因此从第一列开始写入
                for i in range(len(movie_info)-1):#对于一行信息进行遍历，分别存入每列
                    sheet.write(row,i,movie_info[i+1])

            sql = "select id,name,sex,star,date_format(from_days(to_days(now())-to_days(birthday)),'%Y')+0,place,job,message from actors"
            cur.execute(sql)
            row = 0
            for actor_info in cur.fetchall():  # 遍历数据库中每行信息，一行表示一部电影的所有信息
                row = row + 1  # 第0行为表头，不添加数据，因此从第一列开始写入
                for i in range(len(actor_info) - 1):  # 对于一行信息进行遍历，分别存入每列
                    sheet2.write(row, i, actor_info[i + 1])

            xls.save(file_name)#写入完成，存储
            cur.close()
            conn.close()

            wx.MessageBox('数据已导出到桌面！！！',caption="导出成功")
        except:
            wx.MessageBox('数据导出失败！！！',caption="导出失败")

    def GetDesktopPath(self):#获取桌面路径
        return os.path.join(os.path.expanduser("~"), 'Desktop')

    def count_type(self):#统计电影类型数量
        conn = pymysql.connect(host='localhost',user='root',password='970922',db='mytest',port=3306,charset='utf8')
        #从数据库中获取数据
        cur = conn.cursor()
        sql = 'select movie_type from movies'#只查询电影0类型
        cur.execute(sql)
        movie_type_list = []#存储已知的电影类型
        movie_count_type = dict()#定义字典，表示电影类型对应的数量
        for movie_type_row in cur.fetchall():#遍历查询结果
            movie_types = movie_type_row[0]#获取该电影属于哪些分类
            # print(movie_types)
            movie_type_list += movie_types.split("/")#因为一部电影可能属于多种分类，因此用分隔符 ‘/’ 分开，然后将得到的list全部加入类型list中
        for movie_type in movie_type_list:#最后将收集到的所有类型进行字典计数
            if movie_type not in movie_count_type:#如果是字典中不存在的类型，那么计数为初始计数为1
                movie_count_type[movie_type] = 1
            else:
                movie_count_type[movie_type] += 1#否则计数加1
        print(movie_count_type)#输出统计结果
        return movie_count_type#返回字典

    def matplotlib_show(self,movie_count_type):
        #指定默认字体
        plt.cla()
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['font.family']='sans-serif'
        matplotlib.rcParams['axes.unicode_minus'] = False
        count = []#数量
        category = []#类型
        for movie_type in movie_count_type:#遍历电影类型计数
            count.append(movie_count_type[movie_type])
            category.append(str(movie_type))
        new_count=count
        y_pos = np.arange(len(category))
        plt.bar(y_pos, count, align='center', alpha=0.7)
        plt.xticks(y_pos, category)

        for count, y_pos in zip(count, y_pos):
            plt.text(y_pos, count+0.5, count,  horizontalalignment='center', verticalalignment='center', weight='bold')
        plt.title('电影类别数据分析')#图标标题
        plt.xlabel(u'电影分类')
        plt.subplots_adjust(bottom = 0.15)
        plt.ylabel(u'分类出现次数')

        try:
            savePath = self.GetDesktopPath() + "\\电影类别数据直方图.png"  # 将结果图存储到桌面
            plt.savefig(savePath)
            showDataPic = Save_Show_Pic.ShowDataPic(None,openPath=savePath)
            showDataPic.Show(True)
            # wx.MessageBox('数据图已导出到桌面！！！', caption="导出成功")
        except:
            wx.MessageBox('数据图导出失败！！！', caption="导出失败")
        plt.cla()
        sum_count = sum(new_count)
        sizes = []
        for it in new_count:
            sizes.append(it / sum_count)
        plt.pie(sizes, explode=list(0.1 for x in range(len(sizes))), labels=category, autopct="%.2f%%", shadow=True, startangle=90)
        plt.title(r'电影类型比例饼状图', fontproperties="SimHei", fontsize=15)
        try:
            savePath = self.GetDesktopPath() + "\\电影类别数据饼状图.png"  # 将结果图存储到桌面
            plt.savefig(savePath)
            showDataPic2 = Save_Show_Pic.ShowDataPic(None,openPath=savePath)
            showDataPic2.Show(True)
            wx.MessageBox('数据图已导出到桌面！！！', caption="导出成功")
        except:
            wx.MessageBox('数据图导出失败！！！', caption="导出失败")

    def matplotlib_show2(self):
        conn = pymysql.connect(host='localhost', user='root', password='970922', db='mytest', port=3306, charset='utf8')
        # 从数据库中获取数据
        cur = conn.cursor()
        sql = 'select thread_num,times from data_log where data_num>=40 and data_num<=42'  # 查询爬取相同数据下，线程与时间关系
        cur.execute(sql)
        thread_nums=[]
        time_cnt=[]
        for it in cur.fetchall():
            thread_nums.append(it[0])
            time_cnt.append(it[1])
        plt.cla()
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['font.family'] = 'sans-serif'
        plt.title(r'线程数-时间散点图（数据量为40~42时）', fontproperties="SimHei", fontsize=15)

        plt.xlabel('线程数量')
        plt.ylabel('时间')
        plt.xlim(0, 6)
        plt.scatter(thread_nums, time_cnt, s=20, c="#ff1212", marker='*')
        try:
            savePath = self.GetDesktopPath() + "\\线程-时间数据散点图.png"  # 将结果图存储到桌面
            plt.savefig(savePath)
            showDataPic2 = Save_Show_Pic.ShowDataPic(None, openPath=savePath)
            showDataPic2.Show(True)
            # wx.MessageBox('数据图已导出到桌面！！！', caption="导出成功")
        except:
            wx.MessageBox('数据图导出失败！！！', caption="导出失败")

        sql = 'select data_num,times from data_log where thread_num=3'  # 查询爬取相同数据下，线程与时间关系
        cur.execute(sql)
        data_cnt = []
        time_cnt2 = []
        for it in cur.fetchall():
            data_cnt.append(it[0])
            time_cnt2.append(it[1])
            # print(it)
        plt.cla()
        plt.title(r'数量-时间散点图（同为3线程数）', fontproperties="SimHei", fontsize=15)

        plt.xlabel('电影数量')
        plt.ylabel('时间')
        plt.xlim(0, 100)
        plt.scatter(data_cnt, time_cnt2, s=20, c="#ff1212", marker='+')
        try:
            savePath = self.GetDesktopPath() + "\\数量-时间数据散点图.png"  # 将结果图存储到桌面
            plt.savefig(savePath)
            showDataPic2 = Save_Show_Pic.ShowDataPic(None, openPath=savePath)
            showDataPic2.Show(True)
            wx.MessageBox('数据图已导出到桌面！！！', caption="导出成功")
        except:
            wx.MessageBox('数据图导出失败！！！', caption="导出失败")



if __name__=='__main__':
    app = wx.App()
    spiderClient = SpiderClient(None)
    spiderClient.Show()
    app.MainLoop()
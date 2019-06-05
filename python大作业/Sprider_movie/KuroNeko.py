import wx
import KuroNeko_Spider_Server
import threading
from Login_to_Spider import loginFrame

if __name__ == '__main__':
    #开启客户端
    s=KuroNeko_Spider_Server.SpiderServer()#开启服务器
    threading.Thread(target=s.startServer, args=()).start()#如果做B/S结构，服务器端应单独开启，不受任何客户端控制，客户端有多个可以与服务器端交互
    app = wx.App()
    LoginFrame = loginFrame(None)
    LoginFrame.Show()
    app.MainLoop()

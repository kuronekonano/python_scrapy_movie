import json
import pickle
import socket
import threading

from Spider_Engine import Spider#此处导入爬虫模块，也就是说这个爬虫服务必须先开启，并且客户端是通过爬虫服务器来启动和获取爬取结果

class SpiderServer(object):
    def __init__(self):
        pass

    def startServer(self):
        print("(:з」∠)_服务器：又要起床做事了ヾ(ｏ・ω・)ノ！！！")
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(('localhost',12306))
        s.listen(5)
        while True:
            conn,addr = s.accept()#conn用于与客户端进行通信
            page_info = conn.recv(1024)
            if not page_info:
                continue
            print(pickle.loads(page_info))#输出从客户端发送过来的爬取要求，读取byte
            page_info = pickle.loads(page_info)
            # page_info[movie_type,movie_sort,threadNum,pageNum,query_type]
            threading.Thread(target=Spider().startSpiderInfo,args=(page_info,conn,)).start()#此处启动线程调用了爬虫模块，并用conn作为参数，使得爬虫模块也能直接与客户端进行通信
            conn.sendall("服务器：我被找到了(｡>∀<｡)！！！\n".encode())#以 encoding 指定的编码格式编码字符串
        conn.close()
        s.close()
#开启服务器
if __name__=='__main__':
    s = SpiderServer()
    s.startServer()

# function_name: 需要线程去执行的方法名
# threading.Thread()创建线程.start()并启动线程
# args: 线程执行方法接收的参数，该属性是一个元组，如果只有一个参数也需要在末尾加逗号
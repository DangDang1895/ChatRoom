#-*- coding:utf-8-*-
import socket
import threading
import struct
from common import packData, HEART_BEAT,NORMAL,HEADERSIZE
import time
import sys
#创建socket对象
s = socket.socket()
#端口号和IP
serverIP = '127.0.0.1'
serverPort = 10086
#连接远程主机
s.connect((serverIP,serverPort))
heartBeatCount = 0



def sendHeartBeat():
    global heartBeatCount
    while True:
        time.sleep(30)
        print(">>客户端发送心跳包, Are you ok!")
        s.send(packData(b'Are you ok!', HEART_BEAT))
        heartBeatCount = heartBeatCount + 1
        if heartBeatCount>3:
            print(">>ERROR: 心跳检测发现问题")
        


# 处理接收到的数据包
def dealData(headPack, body):
    global heartBeatCount
    # 数据包类型为HEART_BEAT时
    if headPack[1] == HEART_BEAT:
        print('>>客户端收到服务端返回心跳包, Ok!')
        heartBeatCount = heartBeatCount -1
    else:
        body=body.decode('utf-8')
        print(body)








def receive():
    dataBuffer = bytes()
    while True:
        try:
            data=s.recv(1024)
        except  socket.error:
            print(">>服务器已经关闭!")
            sys.exit("服务器已经关闭!") 
        if data:
            dataBuffer += data

        while len(dataBuffer) > HEADERSIZE:
            headPack = struct.unpack('!3I', dataBuffer[:HEADERSIZE])
            bodySize = headPack[2]

            if len(dataBuffer) < HEADERSIZE+bodySize:
                print("数据包（%s Byte）不完整（总共%s Byte），继续接受 " % (len(dataBuffer), HEADERSIZE+bodySize))
                break

            body = dataBuffer[HEADERSIZE:HEADERSIZE+bodySize]
            dealData(headPack, body)
                
            dataBuffer = dataBuffer[HEADERSIZE+bodySize:]
                

            
            


        
threading.Thread(target=receive).start()

threading.Thread(target=sendHeartBeat).start()



# 向服务端发送数据
while True:
    s.send(packData(input().encode('utf-8'),NORMAL))
   
   
time.sleep(5)











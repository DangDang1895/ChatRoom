#-*- coding:utf-8-*-
import struct
import socket
import threading
#定义保存所有socket的列表
import select
from common import packData, HEART_BEAT,NORMAL,HEADERSIZE

#创建socket对象
serverSocket = socket.socket()
#将socket绑定到本机IP和端口
serverSocket.bind(('127.0.0.1',10086))
#服务端开始监听来自客户端的连接
serverSocket.listen()
online_users = []
# 最大连接数为5
serverSocket.listen(500) 
print("The server is ready to receive")


def tcplink(conn,addr):
    print('Accept new connection from %s:%s...' % addr)
    
    message_come ='>>用户'+str(addr)+'加入了聊天室'
    for J in online_users:
        J.send(packData(message_come.encode('utf-8'),NORMAL))
    
    X='>>当前在线'+str(len(online_users))+'人'
    for K in online_users:
        K.send(packData(X.encode('utf-8'),NORMAL))
        
    dataBuffer = bytes()
    while True:
        connect=True
        try:
            data = conn.recv(1024)
            if data:
                dataBuffer += data
        except  socket.error:
            connect=False
        else:
            pass
        if connect:
            while len(dataBuffer) > HEADERSIZE:
                headPack = struct.unpack('!3I', dataBuffer[:HEADERSIZE])
                bodySize = headPack[2]

                if len(dataBuffer) < HEADERSIZE+bodySize:
                    print("数据包（%s Byte）不完整（总共%s Byte），继续接受 " % (len(dataBuffer), HEADERSIZE+bodySize))
                    break
                
                body = dataBuffer[HEADERSIZE:HEADERSIZE+bodySize]
                
                if headPack[1] == HEART_BEAT:
                    conn.send(packData(b'>>Ok!',HEART_BEAT))
                else:
                    body=body.decode('utf-8')
                    print('Server received: %s' % body)
                    if body is None:
                        break
                    print('Server sent: %s' % (str(addr)+'： '+body) )
                    for i in online_users:
                        if i is not conn:
                            i.send(packData(('>>'+str(addr)+'： '+body).encode('utf-8'),NORMAL))
                dataBuffer = dataBuffer[HEADERSIZE+bodySize:]
        else:
            conn.close()
            online_users.remove(conn)
            message ='用户'+str(addr)+'离开了聊天室'
            print(message)
            for j in online_users:
                j.send(packData(message.encode('utf-8'),NORMAL))
            
            Y='>>当前在线'+str(len(online_users))+'人'
            for k in online_users:
                k.send(packData(Y.encode('utf-8'),NORMAL))
            break
    

             
        
while True:
    conn,addr = serverSocket.accept()
    online_users.append(conn)
    t=threading.Thread(target=tcplink,args=(conn,addr))
    t.start()






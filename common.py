import struct

HEADERSIZE = 12
HEART_BEAT = 0
NORMAL=1

def packData(data, packetType):
    # 定义数据包头部由版本号和包长三个4位无符号整数组成
    # 它们分别是 版本号 消息类型 包长度
    # 其中 packetType=0 为心跳检测包 packetType=1 为普通消息
    version = 1
    bodyLen = len(data)
    header = [version, packetType, bodyLen]   
    headPack = struct.pack("!3I", *header) # !代表网络字节顺序NBO（Network Byte Order），3I代表3个unsigned int数据
    return headPack + data

import socket
import sys

PORT = 55555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

#接続
try:
    #home
    client.connect(("xxx.xxx.xxx.xxx",PORT))

except:
    print("接続できません")
    sys.exit()

#受信
while(1):
    data = client.recv(1024)
    data = data.decode('utf-8')
    print("Server>", data)

    if len(data) > 3:
        f = open('num.txt','w')
        f.write(data)
        f.close()

    if data == "q":             # qが押されたら終了
        client.close()
        break
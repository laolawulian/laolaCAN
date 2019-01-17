import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json,random,base64

HOST = "xx.xx.xx.xx"    #包含要连接的代理地址
PORT = 1883             #要连接到代理的端口。 默认为1883

def on_connect(client,userdata,flags,rc):
    print("Connected with result code " + str(rc))
    client.subscribe("application/[appEUI]/node/[devEUI]/msg",1)

def on_message(client,userdata,msg):
    print(msg.topic + " " + msg.payload.decode("utf-8"))

if __name__ == '__main__':
    client_id = "20190115102204"    #在开放平台添加勾选MQTT协议的应用产生的client_id
    client = mqtt.Client(client_id) 
    client.username_pw_set("xxxxxxxxxxxxxxxx","xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST,PORT,60)

# 随机产生24位reference值
    list01 = random.sample("zyxwvutsrqponmlkjihgfedcba1234567890",24)
    str01 = ''.join(list01)

# 随机产生1~223之间的fPort值
    fport01 = str(random.randint(1,223))

# 当在开放平台添加不支持通过Encode发送下行消息的数据的应用application使用，随机产生1~24位base64加密后data值
    # m = random.randint(1,24) 
    # list02 = random.sample("zyxwvutsrqponmlkjihgfedcba1234567890zyxwvutsrqponmlkjihgfedcba1234567890",m)
    # str02 = ''.join(list02)
    # data01 = base64.b64encode(str02.encode("utf-8"))
    # base64data = str(data01,"utf-8")

# 当在开放平台添加支持通过Encode发送下行消息的数据的应用application使用，根据Encode格式内容发送的base64加密后data值
    n = random.randint(1,5)
    str03 = {"period":n}
    strdata = json.dumps(str03)
    strdatause = base64.b64encode(strdata.encode("utf-8"))
    base64data01 =  str(strdatause,"utf-8")
# 方式一：向终端发送下行消息数据
    client.publish("application/[appEUI]/node/[devEUI]/tx",
    payload='{"confirmed":true,"data":"'+base64data01+'","devEUI":"xxxxxxxxxxxxxxxx","fPort":'+fport01+',"reference":"'+str01+'"}',
    qos=1,retain=False)

# 方式二：向终端发送下行消息数据
    # publish.single("application/[appEUI]/node/[devEUI]/tx",
    # payload='{"confirmed":true,"data":"'+base64data+'","devEUI":"xxxxxxxxxxxxxxxx","fPort":'+fport01+',"reference":"'+str01+'"}',
    # qos=1,hostname=HOST,port=PORT,client_id=client_id,
    # auth={'username':"xxxxxxxxxxxxxxxx",'password':"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"})

    
    
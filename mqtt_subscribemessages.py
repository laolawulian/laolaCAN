import paho.mqtt.client as mqtt

HOST = "xx.xx.xx.xx"    #包含要连接的代理地址
PORT = 1883             #要连接到代理的端口。 默认为1883

def client_loop():
    client_id = "20190115102204"    #在开放平台添加勾选MQTT协议的应用产生的client_id
    client = mqtt.Client(client_id=client_id,clean_session=False)
    client.username_pw_set("xxxxxxxxxxxxx","xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")  #在开放平台添加勾选MQTT协议的应用产生的username，password
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST,PORT,60)
    client.loop_forever() 
    
def on_connect(client,userdata,flags,rc):
    print("Connected with result code "+ str(rc))
    client.subscribe("application/{appEUI}/node/{devEUI}/msg",0)    #subscribe(topic,qos)，qos根据用户需要进行选取，(qos=0最多一次，qos=1至少一次，qos=2有且只有一次）

def on_message(lient,userdata,msg):
    print(msg.topic +"\n" + msg.payload.decode("utf-8"))
    

if __name__ == '__main__':
    client_loop()

   
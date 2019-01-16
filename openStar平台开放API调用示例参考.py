import requests,json
import time
import hashlib
import random
import string
import base64

HOST = "openapi.loraiot.cn"   
#4.1登录获取token
def login():
    url="http://"+HOST+"/login"
    headers = {"Content-Type":"application/json","Connection":"close"}
    pyload={"username":"xxxxxxxxxxx","password":"xxxxxxxxxx"}
    r=requests.post(url,headers=headers,data=json.dumps(pyload))
    content = r.text
    # print ("-----用户登录content-----'\n'",content)
    con1 = content.split('"')
    # print ("-----登录返回截取的token内容-----'\n'",con1[7])
    logintoken = con1[7]
    return logintoken
    
#4.2登录获取刷新token
def refresh_token(func):
    url="http://"+HOST+"/refresh_token"
    headers = {"Authorization":func}
    r=requests.post(url,headers=headers)
    print ("-----刷新登录token-----'\n'",r.text)

#通用添加headers方法
def add_headers(func,send_method,bodyStr,AppEUI,AppSecret):
    host = HOST
    t = str(int(time.time()))
    pyloads = json.dumps(pyload)

#LOLA-ACCESS-SIGNATURE加密
    str1 = ('%s%s%s%s%s')%(t,send_method,host,pyloads,AppSecret)
    secretStr = hashlib.md5(str1.encode('utf-8')).hexdigest()
    headers = {
        'Authorization':'Bearer '+func,
        'LOLA-ACCESS-APPID':AppEUI,
        'LOLA-ACCESS-NONCE':t,
        'LOLA-ACCESS-SIGNATURE':secretStr,
        'Content-Type':'application/json'
    }
    return headers

#4.3自定义下行数据
def add_downlink(func,bodyStr,devEUI):
    url="http://"+HOST+"/openapi/devices/tx/"+devEUI
    r=requests.post(url,headers=func,data=bodyStr)
    print ("-----自定义下行数据-----'\n'",r.text)   

#4.5添加终端设备
def add_device(func,bodyStr):  
    url="http://"+HOST+"/openapi/devices/relation"
    r=requests.post(url,headers=func,data=bodyStr)
    print ("-----添加终端设备-----'\n'",r.text)
    

#4.6删除设备
def delete_device(func,bodyStr,devEUI):
    url="http://"+HOST+"/openapi/devices/relation/"+devEUI
    r=requests.delete(url,headers=func,data=bodyStr)
    print ("-----删除设备-----'\n'",r.text)

#4.7获取传感器基本信息
def get_deviceinfo(func,bodyStr,devEUI):
    url="http://"+HOST+"/openapi/devices/"+devEUI
    r=requests.get(url,headers=func,data=bodyStr)
    print ("-----获取传感器基本信息-----'\n'",r.text)

#4.8获取传感器数据列表
def get_devicelist(func,bodyStr):
    url = "http://"+HOST+"/openapi/devices?page=1&count=100"
    r=requests.get(url,headers=func,data=bodyStr)
    print ("-----获取传感器数据列表-----'\n'",r.text)

#4.9获取传感器应用数据
def get_appinfo(func,bodyStr,devEUI):
    url = "http://"+HOST+"/openapi/log/"+devEUI+"?page=1&count=100"
    r=requests.get(url,headers=func,data=bodyStr)
    print ("-----获取传感器应用数据-----'\n'",r.text)

if __name__ == '__main__' :
#4.1用户登录获取token
    # login()    

# 4.2刷新token
    # refresh_token(func=login()) 

# 4.3自定义下行数据
    # k = 0
    # while (1!=0):
    #     n = k%10+1
    #     k = k+1
        # list01 = random.sample("zyxwvutsrqponmlkjihgfedcba1234567890",24)
        # str01 = ''.join(list01)
        # fport01 = random.randint(1,223)

    # 应用不支持下行事件时pyload中的data值
        # list02 = random.sample("zyxwvutsrqponmlkjihgfedcba1234567890zyxwvutsrqponmlkjihgfedcba1234567890",n)
        # str02 = ''.join(list02)
        # data01 = base64.b64encode(str02.encode("utf-8"))
        # base64data = str(data01,"utf-8")

    # 应用支持下行事件时pyload中的data值
    #     str03 = {"period":n}
    #     strdata = json.dumps(str03)
    #     strdatause = base64.b64encode(strdata.encode("utf-8"))
    #     base64data01 =  str(strdatause,"utf-8")
       
        # pyload = {
        #     "data":base64data01,
        #     "reference":str01,
        #     "fport":fport01,
        #     "confirmed":False
        # }

    #     pyloads = json.dumps(pyload) 
    #     add_downlink(func=add_headers(func=login(),send_method="POST",bodyStr=pyload,AppEUI="xxxxxxxxxxxxxxxx",AppSecret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),bodyStr=pyloads,devEUI="xxxxxxxxxxxxxxxx")
    #     time.sleep(5)


#4.5添加设备：
    # pyload = {                                           
    #  "device_name":"测试",
    #  "device_model":3,
    #  "device_active_mode":2,
    #  "device_eui":"xxxxxxxxxxxxxxxx",
    #  "device_appkey":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    #  "device_nwksKey":"",
    #  "device_appsKey":"",
    #  "device_addr":"",
    #  "band":"CN_470_510",
    #  "protocol_version":1,
    #  "rx_window":1,
    #  "rx1_dr_offset":1,
    #  "rx_delay":1,
    #  "rx2_dr":1
    # }
    # pyloads = json.dumps(pyload) 

    # add_device(func=add_headers(func=login(),send_method="POST",bodyStr=pyload,AppEUI="xxxxxxxxxxxxxxxx",AppSecret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),bodyStr=pyloads)

#4.6删除设备
    # pyloads = json.dumps(pyload)
    # delete_device(func=add_headers(func=login(),send_method="DELETE",bodyStr=pyload,AppEUI="xxxxxxxxxxxxxxxx",AppSecret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),bodyStr=pyloads,devEUI="xxxxxxxxxxxxxxxx")

#4.7获取传感器基本信息
    # pyload = {}
    # pyloads = json.dumps(pyload)
    # get_deviceinfo(func=add_headers(func=login(),send_method="GET",bodyStr=pyload,AppEUI="xxxxxxxxxxxxxxxx",AppSecret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),bodyStr=pyloads,devEUI="xxxxxxxxxxxxxxxx")

#4.8获取传感器数据列表
    # pyload = {}
    # pyloads = json.dumps(pyload)
    # get_devicelist(func=add_headers(func=login(),send_method="GET",bodyStr=pyload,AppEUI="xxxxxxxxxxxxxxxx",AppSecret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),bodyStr=pyloads)

#4.9获取传感器应用数据
    pyload = {}
    pyloads = json.dumps(pyload)
    get_appinfo(func=add_headers(func=login(),send_method="GET",bodyStr=pyload,AppEUI="xxxxxxxxxxxxxxxx",AppSecret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),bodyStr=pyloads,devEUI="xxxxxxxxxxxxxxxx")
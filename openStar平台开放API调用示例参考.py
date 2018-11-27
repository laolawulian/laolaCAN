import requests,json
import time
import hashlib

#4.1登录获取token
def login():
    url="http://openapi.loraiot.cn/login"
    headers = {"Content-Type":"application/json"}
    pyload={"username":"xxxxxxxxxxx","password":"xxxxxxxxxx"} #在前端通过手机号注册的用户名密码
    r=requests.post(url,headers=headers,data=json.dumps(pyload))
    #print ("-----用户登录-----'\n'",r.text)
    return r

#登录截取token内容
def obtain_token(func):
    content = func.text
    con1 = content.split('"')
    #print ("-----登录返回截取的token内容-----'\n'",con1[7])
    return con1[7]
    
#4.2登录获取刷新token
def refresh_token(func):
    url="http://openapi.loraiot.cn/refresh_token"
    headers = {"Authorization":func}
    r=requests.post(url,headers=headers)
    #print ("-----刷新登录token-----'\n'",r.text)

#通用添加headers方法
def add_headers(func,send_method,bodyStr,AppEUI,AppSecret):
    HOST = "openapi.loraiot.cn"
    t = str(int(time.time()))
    pyloads = json.dumps(pyload)

#LOLA-ACCESS-SIGNATURE加密
    str1 = ('%s%s%s%s%s')%(t,send_method,HOST,pyloads,AppSecret)
    secretStr = hashlib.md5(str1.encode('utf-8')).hexdigest()
    headers = {
        'Authorization':'Bearer '+func,
        'LOLA-ACCESS-APPID':AppEUI,
        'LOLA-ACCESS-NONCE':t,
        'LOLA-ACCESS-SIGNATURE':secretStr,
        'Content-Type':'application/json'
    }
    return headers
    

#4.4添加终端设备
def add_device(func,bodyStr):  
    url="http://openapi.loraiot.cn/openapi/devices/relation"
    r=requests.post(url,headers=func,data=bodyStr)
    print ("-----添加终端设备-----'\n'",r.text)
    
#4.3自定义下行数据
def add_downlink(func,bodyStr,devEUI):
    url="http://openapi.loraiot.cn/openapi/devices/tx/"+devEUI
    r=requests.post(url,headers=func,data=bodyStr)
    print ("-----自定义下行数据-----'\n'",r.text)

#4.5删除设备
def delete_device(func,bodyStr,devEUI):
    url="http://openapi.loraiot.cn/openapi/devices/relation/"+devEUI
    r=requests.delete(url,headers=func,data=bodyStr)
    print ("-----删除设备-----'\n'",r.text)

#4.6获取传感器基本信息
def get_deviceinfo(func,bodyStr,devEUI):
    url="http://openapi.loraiot.cn/openapi/devices/"+devEUI
    r=requests.get(url,headers=func,data=bodyStr)
    print ("-----获取传感器基本信息-----'\n'",r.text)

#4.7获取传感器数据列表
def get_devicelist(func,bodyStr):
    url = "http://openapi.loraiot.cn/openapi/devices?page_index=1&page_size=100"
    r=requests.get(url,headers=func,data=bodyStr)
    print ("-----获取传感器数据列表-----'\n'",r.text)

#4.8获取传感器应用数据
def get_appinfo(func,bodyStr,devEUI):
    url = "http://openapi.loraiot.cn/openapi/log/"+devEUI+"?page=1&count=100"
    r=requests.get(url,headers=func,data=bodyStr)
    print ("-----获取传感器应用数据-----'\n'",r.text)

if __name__ == '__main__' :
#4.1用户登录获取token
    #login()    
    #obtain_token(func=login()) #获取token

#4.2刷新token
    #refresh_token(func=obtain_token(func=login())) 

#4.4添加设备：
    # pyload = {                                           
    #  "device_name":"设备88",
    #  "device_model":3,
    #  "device_active_mode":1,
    #  "device_eui":"5011000010fff203",
    #  "device_appkey":"98929B92f09e2daf676d646d0f61d218",
    #  "device_nwksKey":"98929B92f09e2daf676d646d0f61d210",
    #  "device_appsKey":"98929B92f09e2daf676d646d0f61d215",
    #  "device_addr":"00110000",
    #  "band":"CN_470_510",
    #  "protocol_version":1,
    #  "rx_window":1,
    #  "rx1_dr_offset":1,
    #  "rx_delay":1,
    #  "rx2_dr":1
    # }
    # pyloads = json.dumps(pyload) 

    # add_device(func=add_headers(func=obtain_token(func=login()),send_method="POST",bodyStr=pyload,AppEUI="dd1f46a34d97b09b",AppSecret="D2F18680BA4B4C7543A73AB02712F5A5"),bodyStr=pyloads)

#4.3自定义下行数据

    # pyload = {
    #     "data":"MTIzNDU2N3l0cmV3cQ==",
    #     "reference":"9912w5ertyui45678dfghjkv",
    #     "fport":96,
    #     "confirmed":True
    # }

    # pyloads = json.dumps(pyload) 

    # add_downlink(func=add_headers(func=obtain_token(func=login()),send_method="POST",bodyStr=pyload,AppEUI="dd1f46a34707b09b",AppSecret="D2F1F680BA4B4C7543A73AB02712F5A5"),bodyStr=pyloads,devEUI="0011000019ffffff")

#4.5删除设备
    # pyload = {}
    # pyloads = json.dumps(pyload)
    # delete_device(func=add_headers(func=obtain_token(func=login()),send_method="DELETE",bodyStr=pyload,AppEUI="dd1f46a34807b09b",AppSecret="D2F9F680BA4B4C7543A73AB02712F5A5"),bodyStr=pyloads,devEUI="5011900010fff203")

#4.6获取传感器基本信息
    # pyload = {}
    # pyloads = json.dumps(pyload)
    # get_deviceinfo(func=add_headers(func=obtain_token(func=login()),send_method="GET",bodyStr=pyload,AppEUI="dd1f46a38d07b09b",AppSecret="D2F19687BA4B4C7543A78AB02712F5A5"),bodyStr=pyloads,devEUI="5001009010fff209")

#4.7获取传感器数据列表
    # pyload = {}
    # pyloads = json.dumps(pyload)
    # get_devicelist(func=add_headers(func=obtain_token(func=login()),send_method="GET",bodyStr=pyload,AppEUI="dd1f46a34d08b09b",AppSecret="D2F1F880BA4B4C7543873AB02712F5A5"),bodyStr=pyloads)

#4.8获取传感器应用数据
    pyload = {}
    pyloads = json.dumps(pyload)
    get_appinfo(func=add_headers(func=obtain_token(func=login()),send_method="GET",bodyStr=pyload,AppEUI="dd7f46a34d07b09b",AppSecret="D2F18680BA9B4C7543A73AB02712F5A5"),bodyStr=pyloads,devEUI="0011009010ffffff")
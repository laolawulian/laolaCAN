<!-- TOC -->

- [概述](#概述)
- [1. 开放平台接口说明](#1-开放平台接口说明)
    - [1.1. API权限检验](#11-api权限检验)
    - [1.2. 相关参数说明](#12-相关参数说明)
    - [1.3. 安全模式加解密算法说明](#13-安全模式加解密算法说明)
- [2. Webhook](#2-webhook)
    - [2.1. 填写服务器配置](#21-填写服务器配置)
    - [2.2. 推送数据业务序列图](#22-推送数据业务序列图)
    - [2.3. 接收响应](#23-接收响应)
- [3. MQTT](#3-mqtt)
    - [3.1. 客户端设置](#31-客户端设置)
    - [3.2. 数据交互topic](#32-数据交互topic)
    - [3.3. 推送数据业务序列图](#33-推送数据业务序列图)
- [4. 开放API说明](#4-开放api说明)
    - [4.1. 登陆获取Token](#41-登陆获取token)
    - [4.2. 刷新Token](#42-刷新token)
    - [4.3. 自定义下行数据](#43-自定义下行数据)
    - [4.4. 关联设备到应用（应用添加设备）](#44-关联设备到应用(应用添加设备)
    - [4.5. 解除设备与应用的关联关系（删除设备）](#45-解除设备与应用的关联关系(删除设备)
    - [4.6. 获取传感器基本信息](#46-获取传感器基本信息)
    - [4.7. 获取传感器数据列表](#47-获取传感器数据列表)
    - [4.8. 获取传感器应用数据](#48-获取传感器应用数据)

<!-- /TOC -->

# 概述
  Open Star是为了让终端设备厂商通过该平台，为其提供终端设备接入LoRaWAN网络的入口，通过接入Open Star来完成设备入网、实时接收和发送消息的业务，开放给所有通过开发者资质认证后的开发者使用。
该平台提供给第三方开发者三种不同协议配置的方案，开发者可以根据需要进行对接获取终端设备产生的数据，三种协议为：

MQTT协议

Webhook协议

开放API协议(如需对终端设备进行增删改查，添加应用时必选)

# 1. 开放平台接口说明
## 1.1. API权限检验
消息体签名检验是应用开发者与 lola IoT 云平台相互请求的鉴权方式。  

开发者提交 Webhook(自定义回调URL) 地址后，lola发送给开发者的请求设置了 3 个 HTTP Header, 包括LOLA-ACCESS-APPID,LOLA-ACCESS-NONCE 和 LOLA-ACCESS-SIGNATURE。开发者通过检验 signature 对请求进行校验, 来确认此次 POST 请求来自 lola服务器。  

开发者请求 lola IoT 开放 API 接口时，也需要携带以上三个 headers 参数，lola服务器通过检验 signature 对请求进行校验，来确定开发者身份。  

请求携带 headers 参数如下表所示:  

键名 | 名称 | 说明
--- |:---:| ---
LOLA-ACCESS-APPID|AppEUI|开发者应用标示符
LOLA-ACCESS-NONCE|timeStamp|发请求的 Unix 时间，精确到秒
LOLA-ACCESS-SIGNATURE|无|以 AppSecret 作为密钥，计算 LOLA-ACCESS-NONCE + METHOD(POST/GET…) + HOST+ BODY(如果body为空，则有{})+AppSecret 的 HMAC(md5) 的结果
判断用户的请求是否超时，即服务器收到请求的时间需要符合以下要求：  
- {timestamp} - 5分钟 < 服务器接收到请求时间 < {timestamp} + {expirationPeriodInSeconds} + 5分钟  
- timestamp代表签名生效UTC时间，expirationPeriodInSeconds代表签名有效期限。  
为了防止用户时钟与服务器时钟不同步而导致的认证失败，此处引入5分钟的宽松系数。如果服务器收到请求的时间不符合以上时间要求，则认为请求超时，拒绝该请求；如果符合上述要求，则执行下一步操作。  

## 1.2. 相关参数说明
开发者后台获取如下参数：  

参数名称|说明
---|---
AppID|开发者应用标示符
AppSecret|消息签名密钥
AppKey|应用数据加密解密秘钥

上述参数在Open Star平台我的应用→查看应用界面显示内容如下：

![GitHub](https://yoki-1257355505.cos.ap-beijing.myqcloud.com/%E5%8F%82%E7%85%A7%E5%9B%BE%E7%89%87-01.png "GitHub,Social Coding")

可选择消息加解密方式:  
* 明文模式
* 安全模式

模式的选择与服务器配置在提交后都会立即生效，开发者谨慎填写及选择。加解密方式的默认状态为明文模式，选择安全模式需要提前配置好相关加解密代码。  

## 1.3. 安全模式加解密算法说明
消息加密解密技术方案基于 AES 加解密算法来实现，具体如下: 

1. AppKey 即消息加解密Key，长度固定为16个字符，从a-z,A-Z,0-9共62个字符中选取。由开发者在开发配置中获取，可重新获取。
2. AES 采用 CBC 模式，秘钥长度为 16 个字节（128位），数据采用 PKCS#7 填充； 

  PKCS#7：K 为秘钥字节数（采用16），buf 为待加密的内容，N 为其字节数。Buf 需要被填充为 K 的整数倍。在 buf 的尾部填充 (K-N%K) 个字节，每个字节的内容 是 (K- N%K)。  

 lola向开发者提供开放 API 接口，方便开发者对接 IoT 云平台。

# 2. Webhook
Webhook 的功能是将传感器数据和事件消息通过 HTTP POST 命令实时发送到指定的 URL(服务器)，为保护您的数据安全，请使用 HTTPS URL。  

## 2.1. 填写服务器配置
在平台上填写开发者 Webhook 地址, 其中 URL 必须支持 POST 请求方法，因为数据是通过 POST 的方式推送。  
在平台配置得到对应的 AppEUI, AppKey 和 AppSecret。  

注： 推送数据包括： 传感器上报的实时数据、传感器下行任务的结果、otaa模式入网成功通知。

## 2.2. 推送数据业务序列图
当终端向云平台上传数据包时，lola服务器将 JSON 数据包base64加密 POST 请求到开发者填写的 Webhook 地址。

![img](https://yoki-1257355505.cos.ap-beijing.myqcloud.com/webhook%E5%8D%8F%E8%AE%AE%E5%BA%8F%E5%88%97%E5%9B%BE.png)

第一步：开发者需要注册登录开放平台新增应用获取AppEUI 、AppKey和AppSecret

![img](https://yoki-1257355505.cos.ap-beijing.myqcloud.com/%E6%9F%A5%E7%9C%8B%E5%BA%94%E7%94%A8-01.png)

第二步：在lola开放平台添加ABP/OTAA类型的终端设备

第三步：3rd第三方平台创建webservice服务，接收Content-Type 用text/plain格式，通过webhook协议获取平台和终端推送的数据

第四步：终端入网，为了加入LoRaWAN网络，每个终端需要初始化及激活

终端的激活有两种方式，一种是空中激活 Over-The-Air Activation (OTAA)，当设备部署和重置时使用; 另一种是独立激活 Activation By Personalization (ABP)，此时初始化和激活这两步就在一个步骤内完成。

如果选择添加为otaa设备，设备入网后会推送入网成功消息（abp设备无此入网消息通知），返回数据格式如下：

- 参数举例：

Request

{
    
    "appEUI": "123456789abcdedd",
    
    "devEUI": "aabbccddeeff1122",
    
    "type": "dev_join", // 消息类型
    
    "createdTime": 12343322211122,
    
    "msgId": "abcd1234" //消息 id
}


- 参数说明：

参数说明|是否必有|类型|示例值|说明
---|:---:|:---:|:---:|---
appEUI|是|string|123456789abcdef1|系统分配给应用的唯一标示符
devEUI|是|string|1122334455667788|终端设备标示符, 即传感器或者传输模块的唯一标识
type|是|string|dev_join|设备消息类型
createdTime|是|number    |1490611396441|云平台接收到消息的时间
msgId|是|string|587c90931755e87f7fb41361|消息 Id，为避免重复, 传感器或传输模块上传的每条数据 id 不同

第五步：入网成功后，终端设备通过传感器上报实时数据，返回数据格式如下：

- 参数举例：

Request

{
    
"appEUI": "123456789abcdedd",
    
"devEUI": "aabbccddeeff1122",
    
"type": "dev_msg",                      // 消息类型
    
"createdTime": 12343322211122,
    
"msgId": "abcd1234",                    //消息 id
    
"frequency": 868100000,                 // 频段
    
"rssi": -50,                            // 信号强度
    
"snr": 11.5,                            // 信噪比
    
"transMode": 1,                      // 根据终端数据是否经过解码： 1 透传 2 非透传
    
"fPort": 10,                      // 终端应用数据标识端口
    
"data": "透传模式数据"
    
}

- 参数说明：

参数说明 | 是否必有 | 类型 | 示例值 | 说明 
---- |:----:|:----:|:----:| ---- 
appEUI | 是 | string | 123456789abcdef1 | 系统分配给应用的唯一标示符
devEUI | 是 | string | 1122334455667788| 终端设备标示符, 即传感器或者传输模块的唯一标识
type | 是 | string | dev_msg | 设备消息
createdTime | 是 | number | 1490611396441 | 云平台接收到消息的时间
msgId | 是 | number | 587c90931755e87f7fb41361 | 消息 Id，为避免重复, 传感器或传输模块上传的每条数据 id 不同
frequency | 是 | number | 868100000 | 消息接收的频率
rssi | 是 | number | -50 | 信号强度, 取值范围：[-127,127]
snr | 是 | number | 11.2 | 信噪比，取值范围：[-20, 20]
transMode | 是 | number | 1 | 根据终端数据是否经过解码： 1 透传 2 非透传
fPort | 是 | number | 10 | 终端应用数据标识端口
data  | 是 | string | AAAAAAAA//8= | Base64字符串，明文或者密文

第六步：第三方平台通过开放API（参照4.3 自定义下行数据）推送下行消息给终端


第七步：终端收到确认回复指令为true将返回消息给第三方平台，如终端收到确认回复指令为false，则不返回该消息，返回数据格式如下：

- 参数举例：

Request

{
    
    "appEUI": "123456789abcdedd",
    "devEUI": "aabbccddeeff1122",
    "type": "dev_ack", // 消息类型
    "createdTime": 12343322211122,
    "msgId": "abcd1234", //消息 id
    "reference": "abc211111d1234"
}


- 参数说明：

参数说明|是否必有|类型|示例值|说明
---|:---:|:---:|:---:|---
appEUI | 是 | string | 123456789abcdef1 | 系统分配给应用的唯一标示符
devEUI | 是 | string | 123456789abcdef1 | 终端设备标示符, 即传感器或者传输模块的唯一标识
type     | 是 | string | dev_ack | 设备消息类型
createdTime | 是 | number | 1490611396441 | 云平台接收到消息的时间
msgId | 是 | string |     587c90931755e87f7fb41361 | 消息 Id，为避免重复, 传感器或传输模块上传的每条数据 id 不同
reference | 是 | string | abc211111d1234 | 下行数据唯一引用(可用当前时间戳(毫秒)+六位随机字符)

## 2.3. 接收响应
当开发者服务器接收到请求后，请响应 2xx 的 HTTP 状态码。如果接收到其他 HTTP 状态码，lola会尝试重新推送 3 次，失败 3 次后将不再推送此条数据。  
    
- 返回参数说明  

参数|类型|是否必有|说明
---|:---:|:---:|---
err_code|number|是|错误码 10000为正常，非10000为不正常，3rd可自行定制
err_msg|string|否|"Invalid Params"

lola服务器在 5 秒内收不到响应会断掉连接，并且重新发起请求，总共重试三次。假如服务器无法保证在五秒内处理并回复，可以直接回复空字符串， lola服务器不会对此作任何处理，并且不会发起重试。  

# 3. MQTT

MQTT协议：

MQTT（Message Queuing Telemetry Transport，消息队列遥测传输协议），是一种基于发布/订阅（publish/subscribe）模式的“轻量级”通讯协议, MQTT最大优点在于，可以以极少的代码和有限的带宽，为连接远程设备提供实时可靠的消息服务。做为一种低开销、低带宽占用的即时通讯协议，使其在物联网、小型设备、移动应用等方面有较广泛的应用。


MQTT协议特点：

MQTT协议运行在TCP/IP或其他网络协议，提供有序、无损、双向连接。其特点包括：

1.  使用的发布/订阅消息模式，它提供了一对多消息分发，以实现与应用程序的解耦。

2.  对负载内容屏蔽的消息传输机制。

3.  对传输消息有三种服务质量（QoS）：

 •  最多一次，这一级别会发生消息丢失或重复，消息发布依赖于底层TCP/IP网络。即：<=1

 •  至多一次，这一级别会确保消息到达，但消息可能会重复。即：>=1

 •  只有一次，确保消息只有一次到达。即：＝1。在一些要求比较严格的计费系统中，可以使用此级别

4.  数据传输和协议交换的最小化（协议头部只有2字节），以减少网络流量

5.  通知机制，异常中断时通知传输双方    


MQTT协议实现方式：

![img](https://yoki-1257355505.cos.ap-beijing.myqcloud.com/MQTT%E5%8D%8F%E8%AE%AE%E5%AE%9E%E7%8E%B0%E6%96%B9%E5%BC%8F.png)

- 实现MQTT协议需要：客户端和服务器端
- MQTT协议中有三种身份：发布者（Publish）、代理（Broker）（服务器）、订阅者（Subscribe）。其中，消息的发布者和订阅者都是客户端，消息代理是服务器，消息发布者可以同时是订阅者。
- MQTT传输的消息分为：主题（Topic）和负载（payload）两部分
- Topic，可以理解为消息的类型，订阅者订阅（Subscribe）后，就会收到该主题的消息内容（payload）
- payload，可以理解为消息的内容，是指订阅者具体要使用的内容

开发者可以使用mqtt的方式接收或者推送实时数据，或者二者同时支持。

MQTT 是轻量级基于代理的发布/订阅的消息传输协议，进行低带宽、不可靠或间歇性的通信。MQTT Server 为 MQTT 客户端提供 3.1 兼容版本的 MQTT API 接口连接服务.  

MQTT BROKER IP|端口|是否加密
---|:---:|---
app.mqtt.loraiot.cn|1883|明文传输

## 3.1. 客户端设置
连接 MQTT Server 之前，需要设置 username, password基本参数。 当连接时收到 [Error: Connection refused: Not authorized] 信息时，请确定填写的参数是否正确。  

MQTT 客户端通过 application/[appEUI]/node/[devEUI]/+ , topic 接收传感器数据和下发数据到传感器。

## 3.2. 数据交互topic
1. 3rd MQTT 客户端通过：application/[appEUI]/node/[devEUI]/msg 接收传感器发送的数据和平台的回复数据。  

2. 3rd MQTT 客户端通过： application/[appEUI]/node/[devEUI]/tx 向传感器推送数据。  

## 3.3. 推送数据业务序列图

![img](https://yoki-1257355505.cos.ap-beijing.myqcloud.com/MQTT%E5%8D%8F%E8%AE%AE%E6%8E%A8%E9%80%81%E5%BA%8F%E5%88%97%E5%9B%BE.png)

第一步：开发者需要注册登录开放平台新增应用获取AppEUI 、用户名和密码

![img](https://yoki-1257355505.cos.ap-beijing.myqcloud.com/MQTT-%E5%BA%94%E7%94%A8%E5%8F%82%E7%85%A7%E5%9B%BE.png)

第二步：在lola开放平台添加ABP/OTAA类型的终端设备激活终端消息订阅功能

第三步：终端入网，为了加入LoRaWAN网络，每个终端需要初始化及激活。

终端的激活有两种方式，一种是空中激活 Over-The-Air Activation (OTAA)，当设备部署和重置时使用; 另一种是独立激活 Activation By Personalization (ABP)，此时初始化和激活这两步就在一个步骤内完成。

如果选择添加为otaa设备，设备入网后会推送入网成功消息（abp设备无此入网消息通知），返回数据格式如下：


- 参数举例：

Request

{
    
    "appEUI": "123456789abcdedd",
    "devEUI": "aabbccddeeff1122",
    "type": "dev_join", // 消息类型
    "createdTime": 12343322211122,
    "msgId": "abcd1234" //消息 id
}


- 参数说明：


参数说明 | 是否必有 | 类型 | 示例值 | 说明
--- |:---:|:---:|:---:|---
appEUI |    是 | string | 123456789abcdef1 | 系统分配给应用的唯一标示符
devEUI |    是 | string | 1122334455667788 | 终端设备标示符, 即传感器或者传输模块的唯一标识
type | 是 | string | dev_join |  设备消息类型
createdTime |   是 | number |    1490611396441 | 云平台接收到消息的时间
msgId | 是 | string | 587c90931755e87f7fb41361 | 消息 Id，为避免重复, 传感器或传输模块上传的每条数据 id 不同

第四步：入网成功后，终端设备通过传感器上报实时数据，返回数据格式如下：

- 参数举例：

Request

{
    
"appEUI": "123456789abcdedd",
    
"devEUI": "aabbccddeeff1122",
    
"type": "dev_msg",                      // 消息类型, text 普通消息
    
"createdTime": 12343322211122,
    
"msgId": "abcd1234",                    //消息 id
    
"frequency": 868100000,                 // 频段
    
"rssi": -50,                            // 信号强度
    
"snr": 11.5,                            // 信噪比
    
"transMode": 1,                      // 根据终端数据是否经过解码： 1 透传 2 非透传
    
"fPort": 10,                      // 终端应用数据标识端口
    
"data": "透传模式数据"
    
}

- 参数说明：

参数说明 | 是否必有 | 类型 | 示例值 | 说明
--- |:---:|:---:|:---:| --- 
appEUI |    是 | string | 123456789abcdef1 | 系统分配给应用的唯一标示符
devEUI | 是 | string | 1122334455667788 | 终端设备标示符, 即传感器或者传输模块的唯一标识
type | 是 | string | dev_msg |   设备消息
createdTime |   是 | number |    1490611396441 | 云平台接收到消息的时间
msgId | 是 | number | 587c90931755e87f7fb41361 | 消息 Id，为避免重复, 传感器或传输模块上传的每条数据 id 不同
frequency | 是 | number | 868100000 |    消息接收的频率
rssi |   是 |    number |    -50 | 信号强度, 取值范围：[-127,127]
snr |   是 | number | 11.2 | 信噪比，取值范围：[-20, 20]
transMode | 是 | number | 1 | 根据终端数据是否经过解码： 1 透传 2 非透传
fPort | 是 | number | 10 | 终端应用数据标识端口
data | 是 | string | AAAAAAAA//8= | Base64字符串，明文或者密文

第五步：第三方平台推送下行消息给终端，推送格式说明：

mosquitto_pub -h 指定要连接的域名 -t 指定topic -m 消息内容
-u 指定broker访问用户 -P 指定broker访问密码

推送示例格式如下：

mosquitto_pub -h app.mqtt.loraiot.cn -t application/dd1f46a34d07b09b/node/0011000010ffffff/tx -m "{\
\"confirmed\":true,\

\"data\":\"ZGZkYXNkZmFkZmFkYWRmYWZkYWRhYWQ=\",\

\"devEUI\":\"0011000010ffffff\",\

\"fPort\":24,\	

\"reference\":\"76sdfghj876fghghvn7\" \

}" -u xxxxxxxxxxxxx -P xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

- 消息内容参数说明：

参数说明|是否必有|类型|示例值|说明
---|:---:|:---:|:---:|---
devEUI|是|string|0011000010ffffff|终端设备标示符, 即传感器或者传输模块的唯一标识
fport|是|string|21|LoRaWAN数据端口号（1~223），可用于区分数据类型
confirmed|是|boolean|True/false|下发数据是否需要终端做ack 应答
reference	|是|string|abc211111d1234|下行数据唯一引用(可用当前时间戳(毫秒)+六位随机字符)
data	|是|string|123456789abcdef1|Base64加密

第六步：第三方平台推送下行消息给终端后服务器反馈确认，返回数据格式如下：

- 参数举例：

Request

{
    
    "appEUI": "123456789ABC",
    "devEUI": "123456789ABC",
    "type": "app_ack/app_error",    //event 事件消息app_ack/app_error
    "createdTime": 12343322211122,
    "msgId": "sdfdddfff",           //消息 id
    "reference": "123djcncn56789ABC",
    "msg":"success / error info"
}


- 参数说明：

参数说明 | 是否必有 | 类型 | 示例值 | 说明
--- |:---:|:---:|:---:| ---
appEUI |    是 | string | | 系统分配给应用的唯一标示符
devEUI | 是 | string | |  终端设备标示符, 即传输模块的唯一标识符
type | 是 | string | app_ack/app_error | 当为终端执行云端下发任务的返回值时, type值为”app_ack”,在data中有关于此下发任务的reference
createdTime |   是 | timestamp | | 云平台接收到消息的时间
msgId | 是 | string |      |消息 Id, 为避免重复, 传感器或传输模块上传的每条数据 id 不同
reference    | 是 | string | | 
msg | 是 | string |  | 任务回执消息详情 app_ack时为success，app_error时为错误信息

第七步：终端收到确认回复指令为true将返回消息给第三方平台，如终端收到确认回复指令为false，则不返回该消息。返回数据格式如下：

- 参数举例：

Request


{
    
    "appEUI": "123456789abcdedd",
    "devEUI": "aabbccddeeff1122",
    "type": "dev_ack", // 消息类型
    "createdTime": 12343322211122,
    "msgId": "abcd1234", //消息 id
    "reference": "abc211111d1234"
}


- 参数说明：

参数说明|是否必有|类型|示例值|说明
---|:---:|:---:|:---:|---
appEUI|是|string|123456789abcdef1|系统分配给应用的唯一标示符
devEUI|是|string|123456789abcdef1|终端设备标示符, 即传感器或者传输模块的唯一标识
type|是|string|dev_ack|设备消息类型
createdTime|是|number|1490611396441|云平台接收到消息的时间
msgId|是|string|587c90931755e87f7fb41361|消息 Id，为避免重复, 传感器或传输模块上传的每条数据 id 不同
reference|是|string| abc211111d1234|下行数据唯一引用(可用当前时间戳(毫秒)+六位随机字符)

# 4. 开放API说明


## 4.1. 登陆获取Token

- 接口说明：通过用户名、密码获取token的接口

- 请求说明  

 请求方式  ：POST

 请求地址：http://openapi.loraiot.cn/login

- 请求参数说明  

参数名|类型|是否必填|说明
---|:---:|:---:|---
username|string|Y|用户名(手机号)
password|string|Y|密码

- 返回说明：

正确的返回：

{ 

 "code" : 200,

"expire": "2018-07-29T22:01:29+08:00",

"token":"token内容" 

}


- 返回值说明

参数名|类型|说明
---|:---:|---
code|number|错误值编码
expire|string|过期时间("2018-07-05T16:35:33+08:00")
token|string|签名(JWT)

## 4.2. 刷新Token
- 接口说明：

由于token拥有较短的有效期，当token超时后，可以使用refresh_token进行刷新，refresh_token拥有较长的有效期（30天），当refresh_token失效的后，需要用户重新登录获取token。

- 请求说明：

 请求方式  ：POST

 请求地址  ：http://openapi.loraiot.cn/refresh_token

- Header 说明

Header Key|Header Value|说明
---|:---:|---
Authorization|Bearer {token}|JWT签名

- 请求参数说明  
无

- 返回说明：

 正确的返回：

{ 

"code": 200, 

"expire": "2018-07-29T22:01:29+08:00",

"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbl9ldWlfYXJyIjpbIjAxMTAwMDAwMDAwMDAw

MDEiXSwiZW1haWwiOiJjaGFvLnhpbmdAbG9yYWlvdC5jbiIsImV4cCI6MTUzMDc4MDA2OCwiaWQiOiJ4aW5nY2hhby

IsIm9yaWdfaWF0IjoxNTMwNzc2NDY4LCJzdGF0dXMiOjEsInVzZXJfaWQiOjEsInVzZXJfbmFtZSI6InhpbmdjaGFvIn0.MJ

GghemOcUOfKenaeElJBmQKdkrN9JtW3RpelBE-pwg" 

}

- 返回值说明

参数名|类型|说明
---|:---:|---
code|number|错误值编码
expire|string|过期时间("2018-07-05T16:35:33+08:00")
token|string|签名(JWT)

## 4.3. 自定义下行数据

- 接口说明：
发送确认终端是否返回确认信息数据

- 请求说明：

  请求方式  ：POST

  请求地址  ：http://openapi.loraiot.cn/openapi/devices/tx/devEUI

- 请求Header 说明  

Header Key|Header Value|说明
---|:---:|---
Authorization|Bearer {token}|JWT签名
LOLA-ACCESS-APPID|0110000000000001|开发者应用标示符(AppEUI)
LOLA-ACCESS-NONCE|1530778280|发请求的 Unix 时间，精确到秒
LOLA-ACCESS-SIGNATURE|MD5|以 AppSecret 作为密钥，计算 LOLA-ACCESS-NONCE + METHOD(POST/GET…) + HOST+ BODY(如果body为空，则有{})+AppSecret 的 HMAC(md5) 的结果
Content-Type|application/json|body值类型

- 请求参数说明  

参数名|类型|是否必填|说明
---|:---:|:---:|---
data|string|Y|下发数据内容 base64 sf12/sf1/sf10 小于59bytes; sf9 小于123bytes; sf8/sf7 小于 230bytes
reference|string|Y|唯一标识此下行 为ack 或者error回复 timestamp ns + 8位字符随机数 
fport|number|Y|LoRaWAN数据端口号（1~223），可用于区分数据类型
confirmed|bool|Y|下发数据是否需要终端做ack 应答

- 返回说明：

 正确的返回结果示例：

{

    "code": 0,
    "message": "OK",
    "data": {
        "id": 350,
        "device_eui": "0011000010ffffff",
        "reference": "lslksskskddjdjd2222222261",
        "fport": 23,
        "confirmed": 0,
        "ack_confirmed": 1,
        "downlink_data": "041AFB2FF9866E43E21ABAF59FA7AD5D",
        "createtime": 1532938210,
        "updatetime": 1532938210
    }
}

 错误的返回结果示例：

{

    "code": 20205,
    "message": "fPort字段超出范围",
    "data": null
}


- 返回值说明

参数名|类型|说明
---|:---:|---
code|number|错误值编码
message|string|错误说明
data|object|成功添加数据时,返回所添加的数据实体;失败时返回失败说明;
   
## 4.4. 关联设备到应用（应用添加设备）

- 接口说明：
在已创建的应用下添加终端设备实现传感器等数据监控

- 请求说明：

 请求方式  ：POST

 请求地址  ：http://openapi.loraiot.cn/openapi/devices/relation


- Header 说明  

Header Key|Header Value|说明
---|:---:|---
Authorization|Bearer {token}|JWT签名
LOLA-ACCESS-APPID|0110000000000001|开发者应用标示符(AppEUI)
LOLA-ACCESS-NONCE|1530778280|发请求的 Unix 时间，精确到秒
LOLA-ACCESS-SIGNATURE|MD5|以 AppSecret 作为密钥，计算 LOLA-ACCESS-NONCE + METHOD(POST/GET…) + HOST+ BODY(如果body为空，则有{})+AppSecret 的 HMAC(md5) 的结果
Content-Type|application/json|body值类型

- 请求参数说明  

参数名|类型|是否必填|说明
---|:---:|:---:|---
device_name|string|Y|设备名称
device_model|number|Y|设备模式1: class A, 3: class C 
device_active_mode|number|Y|终端激活方式eg OTAA or ABP ： 1：abp 2: otaa
device_eui|string|Y| 设备全球唯一标识（写在设备中）
device_appkey|string|Y|Lora终端交换密钥,abp模式时为 00000000000000000000000000000000
device_nwksKey|string|N|Lora终端网络密钥 for abp
device_appsKey|string|N|Lora终端应用密钥 for abp
device_addr|string|N|Lora终端固定地址 for abp
band|string|N| 'CN_470_510', 'CN_779_787', 'EU_433'
protocol_version|number|N|1:  LoRaWAN1.0.1, 2:  LoRaWAN1.0.2, 3:  LoRaWAN1.1.0
rx_window|number|N|接收窗口 1:rx1, 2:rx2
rx1_dr_offset|number|N|窗口1数据率飘移
rx_delay|number|N|接收窗口延迟 0s
rx2_dr|number|N| 窗口2数据率 <->sf 10

- 返回说明：

正确的返回结果示例：

  {
    
    "code": 0,
    "message": "OK",
    "data": {
        "id": 576,
        "device_name": "设备",
        "device_model": 1,
        "application_app_eui": "dd1f46a34d07b09b",
        "device_active_mode": 2,
        "device_eui": "0011000010fff2ff",
        "device_appkey": "98929b92f09e2daf676d646d0f61d250",
        "device_nwksKey": "",
        "device_appsKey": "",
        "device_addr": "",
        "band": "CN_470_510",
        "protocol_version": 1,
        "rx_window": 1,
        "rx1_dr_offset": 1,
        "rx_delay": 1,
        "rx2_dr": 1,
        "rx2_frequency": 505300000,
        "battery": 1,
        "signal_strength": 5,
        "createtime": 1532936247,
        "updatetime": 1532936247,
        "last_seen_at": 0
    }
}

错误的返回结果示例：

{

    "code": 20301,
    "message": "基础API未知错误",
    "data": {
        "code": 6,
        "error": "object already exists"
    }
}

- 返回值说明

参数名|类型|说明
---|:---:|---
code|number|错误值编码
message|string|错误说明
data|object|成功添加数据时,返回所添加的数据实体;失败时返回失败说明;

## 4.5. 解除设备与应用的关联关系（删除设备）

- 接口说明：
将已添加的终端设备进行删除

- 请求说明：

  请求方式：DELETE

  请求地址  ：http://openapi.loraiot.cn/openapi/devices/relation/devEUI

- Header 说明  

Header Key|Header Value|说明
---|:---:|---
Authorization|Bearer {token}|JWT签名
LOLA-ACCESS-APPID|0110000000000001|开发者应用标示符(AppEUI)
LOLA-ACCESS-NONCE|1530778280|发请求的 Unix 时间，精确到秒
LOLA-ACCESS-SIGNATURE|MD5|以 AppSecret 作为密钥，计算 LOLA-ACCESS-NONCE + METHOD(POST/GET…) + HOST+ BODY(如果body为空，则有{})+AppSecret 的 HMAC(md5) 的结果
Content-Type|application/json|body值类型

- 请求参数说明  
无

- 返回说明：

正确的返回结果示例：

{

    "code": 0,
    "message": "OK",
    "data": null
}

错误的返回结果示例：

{

    "code": 20204,
    "message": "该设备信息不存在",
    "data": null
}

- 返回值说明

参数名|类型|说明
---|:---:|---
code|number|错误值编码
message|string|错误说明
data|object|null

## 4.6. 获取传感器基本信息

- 接口说明：
获取已添加的终端设备的基本信息

- 请求说明：

 请求方式：GET

 请求地址  http://openapi.loraiot.cn/openapi/devices/devEUI

- Header 说明  

Header Key|Header Value|说明
---|:---:|---
Authorization|Bearer {token}|JWT签名
LOLA-ACCESS-APPID|0110000000000001|开发者应用标示符(AppEUI)
LOLA-ACCESS-NONCE|1530778280|发请求的 Unix 时间，精确到秒
LOLA-ACCESS-SIGNATURE|MD5|以 AppSecret 作为密钥，计算 LOLA-ACCESS-NONCE + METHOD(POST/GET…) + HOST+ BODY(如果body为空，则有{})+AppSecret 的 HMAC(md5) 的结果
Content-Type|application/json|body值类型

- 请求参数说明  
无
    
- 返回说明：

正确的返回结果示例：

{

    "code": 0,
    "message": "OK",
    "data": {
        "id": 575,
        "device_name": "终端设备名称",
        "device_model": 1,
        "application_app_eui": "dd1f46a34d07b09b",
        "device_active_mode": 2,
        "device_eui": "0011000010ffffff",
        "device_appkey": "98929B92f09e2daf676d646d0f61d250",
        "device_nwksKey": "",
        "device_appsKey": "",
        "device_addr": "",
        "band": "CN_470_510",
        "protocol_version": 2,
        "rx_window": 1,
        "rx1_dr_offset": 0,
        "rx_delay": 0,
        "rx2_dr": 0,
        "rx2_frequency": 505300000,
        "battery": 1,
        "signal_strength": 5,
        "createtime": 1532924457,
        "updatetime": 1532924457,
        "last_seen_at": 0
    }
}

错误的返回结果示例：

{

    "code": 403,
    "message": "You don't have permission to access."
}

- 返回值说明

参数名|类型|说明
---|:---:|---
code|number|错误值编码
message|string|错误说明
data|object|device详情

- Data说明

参数名|类型|说明
---|:---:|:---:|---
device_name|string|设备名称
device_model|number|设备模式1: class A, 3: class C 
app_eui|string|应用标识
device_active_mode|number|终端激活方式eg OTAA or ABP ： 1：abp 2: otaa
device_eui|string| 设备全球唯一标识（写在设备中）
device_appkey|string|Lora终端交换密钥 abp时为00000000000000000000000000000000
device_nwksKey|string|Lora终端网络密钥 for abp
device_appsKey|string|Lora终端应用密钥 for abp
device_addr|string|Lora终端固定地址 for abp
band|string| 'CN_470_510', 'CN_779_787', 'EU_433'
protocol_version|number|1:  LoRaWAN1.0.1, 2:  LoRaWAN1.0.2, 3:  LoRaWAN1.1.0
rx_window|number|接收窗口 1:rx1, 2:rx2
rx1_dr_offset|number|窗口1数据率飘移
rx_delay|number|接收窗口延迟 0s
rx2_dr|number| 窗口2数据率 <->sf 10
last_seen_at|number| 最近一条上行数据时间
signal_strength|number|  1:  1格信号 2：2格信号 。。。 5：5格信号

## 4.7. 获取传感器数据列表

- 接口说明：
获取已添加的所属应用下的所有终端设备的信息，分页显示

- 请求说明：

  请求方式  : GET

  请求地址  ：http://openapi.loraiot.cn/openapi/devices?page_index=1&page_size=50

- Header 说明  

Header Key|Header Value|说明
---|:---:|---
Authorization|Bearer {token}|JWT签名
LOLA-ACCESS-APPID|0110000000000001|开发者应用标示符(AppEUI)
LOLA-ACCESS-NONCE|1530778280|发请求的 Unix 时间，精确到秒
LOLA-ACCESS-SIGNATURE|MD5|以 AppSecret 作为密钥，计算 LOLA-ACCESS-NONCE + METHOD(POST/GET…) + HOST+ BODY(如果body为空，则有{})+AppSecret 的 HMAC(md5) 的结果
Content-Type|application/json|body值类型

- 请求参数说明  
参考如上

- 返回说明：

正确的返回结果示例：

{

    "code": 0,
    "message": "OK",
    "data": {
        "device_items": [
            {
                "id": 191,
                "device_name": "设备03",
                "device_model": 1,
                "application_app_eui": "0111100000000001",
                "device_active_mode": 2,
                "device_eui": "3353011411408007",
                "device_appkey": "2b7e151628aed2a6abf7158809cf4f3c",
                "device_nwksKey": "",
                "device_appsKey": "",
                "device_addr": "",
                "band": "CN_470_510",
                "protocol_version": 1,
                "rx_window": 2,
                "rx1_dr_offset": 5,
                "rx_delay": 15,
                "rx2_dr": 4,
                "rx2_frequency": 505300000,
                "battery": 1,
                "signal_strength": 5,
                "createtime": 1532514671,
                "updatetime": 1532940170,
                "last_seen_at": 0
            },
            {
                "id": 192,
                "device_name": "设备02",
                "device_model": 3,
                "application_app_eui": "0111100000000001",
                "device_active_mode": 1,
                "device_eui": "33530114114080a0",
                "device_appkey": "2b7e151628aed2a6abf7158809cf4f36",
                "device_nwksKey": "2b7e151628aed2a6abf7158809cf4f99",
                "device_appsKey": "2b7e151628aed2a6abf7158809cf4f35",
                "device_addr": "1234567e",
                "band": "CN_470_510",
                "protocol_version": 3,
                "rx_window": 2,
                "rx1_dr_offset": 5,
                "rx_delay": 15,
                "rx2_dr": 5,
                "rx2_frequency": 505300000,
                "battery": 1,
                "signal_strength": 5,
                "createtime": 1532514953,
                "updatetime": 1532940160,
                "last_seen_at": 0
            },
            {
                "id": 194,
                "device_name": "设备01",
                "device_model": 3,
                "application_app_eui": "0111100000000001",
                "device_active_mode": 1,
                "device_eui": "335301141140800e",
                "device_appkey": "00000000000000000000000000000000",
                "device_nwksKey": "6ce760532353b434280fa2f7844d5659",
                "device_appsKey": "c4172c3b7f697e6a072788caf4e1e170",
                "device_addr": "0d11876d",
                "band": "CN_470_510",
                "protocol_version": 3,
                "rx_window": 2,
                "rx1_dr_offset": 5,
                "rx_delay": 15,
                "rx2_dr": 5,
                "rx2_frequency": 505300000,
                "battery": 1,
                "signal_strength": 4,
                "createtime": 1532516324,
                "updatetime": 1532940151,
                "last_seen_at": 1532663624
            }
        ],
        "page_info": {
            "current_page": 1,
            "page_size": 20,
            "total_count": 3
        }
    }
}

 错误的返回结果示例：

{

    "code": 403,
    "message": "You don't have permission to access."
}

- 返回值说明

参数名|类型|说明
---|:---:|---
code|number|错误值编码
message|string|错误说明
data|object|device列表

## 4.8.获取传感器应用数据

- 接口说明：
获取已添加的应用的信息，分页显示

- 请求说明：

 请求方式  ：GET

 请求地址  ：http://openapi.loraiot.cn/openapi/log/devEUI?page=1&count=50

- Header 说明  

Header Key|Header Value|说明
---|:---:|---
Authorization|Bearer {token}|JWT签名
LOLA-ACCESS-APPID|0110000000000001|开发者应用标示符(AppEUI)
LOLA-ACCESS-NONCE|1530778280|发请求的 Unix 时间，精确到秒
LOLA-ACCESS-SIGNATURE|MD5|以 AppSecret 作为密钥，计算 LOLA-ACCESS-NONCE + METHOD(POST/GET…) + HOST+ BODY(如果body为空，则有{})+AppSecret 的 HMAC(md5) 的结果
Content-Type|application/json|body值类型
    
- 请求参数说明  
无

- 返回说明：

正确的返回结果示例：

{

    "code": 0,
    "message": "OK",
    "data": {
        "list": [
            {
                "app_eui": "",
                "device_eui": "335301141140800e",
                "sf": 12,
                "frequency": 470500000,
                "fPort": 3,
                "ctime_at": "2017-09-03 15:30:44",
                "data": "dGhpcyBpcyBhIHRlc3Qh",
                "b_analyzed": false
            },
            {
                "app_eui": "",
                "device_eui": "335301141140800e",
                "sf": 12,
                "frequency": 470700000,
                "fPort": 3,
                "ctime_at": "2017-08-17 15:30:56",
                "data": "dGhpcyBpcyBhIHRlc3Qh",
                "b_analyzed": false
            },
            {
                "app_eui": "",
                "device_eui": "335301141140800e",
                "sf": 12,
                "frequency": 471100000,
                "fPort": 3,
                "ctime_at": "2017-08-17 15:31:08",
                "data": "dGhpcyBpcyBhIHRlc3Qh",
                "b_analyzed": false
            }
        ],
        "page_info": {
            "amount": 21005,
            "count": 3,
            "page": 1
        }
    }
}

错误的返回结果示例：

{

    "code": 20204,
    "message": "该设备信息不存在",
    "data": null
}

- 返回值说明

参数名|类型|说明
---|:---:|---
code|number|错误值编码
message|string|错误说明
data|object|appData列表

- data说明

参数名|类型|说明
---|:---:|---
list|array|数据列表
page_info|object|分页信息

- list说明

参数名|类型|说明
---|:---:|---
app_eui|string|应用标识
device_eui|string| 设备全球唯一标识（写在设备中）
frequency|number|消息接收的频率
sf|number|扩频因子
fPort|number|应用端口
ctime_at|string|消息创建时间 (e.g. "2018-07-23 17:51:15")
data|string|应用数据 base64加密
b_analyzed|bool|data数据是否已解码

- page_info说明

参数名|类型|说明
---|:---:|---
amount|number|数据总条数
page|number|当前页码
count|number|当前分页大小




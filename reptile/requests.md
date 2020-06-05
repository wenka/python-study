> 爬虫的定义：是一种按照一定的规则，自动地抓取万维网信息的程序或者脚本。

so:
> 爬虫的第一要素：获取网络资源。

 1. 确定目标网站
 2. 指定目标链接
 3. 确定目标资源
 4. 解析并获取目标

再So：
 **爬虫的第一天：先弄清楚如何发起 http请求。**
 
### ! 请求库
[Requests文档](https://requests.readthedocs.io/en/master/)
```python
import requests
```
##### ？为啥选取 requests 库

```text
文档介绍：Requests 是用于人类的Python优雅而简单的HTTP库。

1. 通过请求，您可以非常轻松地发送HTTP / 1.1请求。 
2. 无需将查询字符串手动添加到您的网址，也无需对POST数据进行表单编码。 
3. 有了urllib3，Keep-alive和HTTP连接池是100％自动的.

本着怎么简单怎么来的原则，果断选择requests。

```

##### ? 如何使用
```python
# 发送GET请求
response = requests.get('url')
response = requests.get('url',params={'key':'value'})
# 发送POST请求
response = requests.post('url',data={'key':'value'})
# 发送PUT请求
response = requests.put('url',data={'key':'value'})
# 发送DELETE请求
response = requests.delete('url')
......
# 更多请查询 api.py
```
Requests 会自动解码服务返回的内容，大多数Unicode字符集都能被无缝的解码！

使用 Requests 发送的请求都将返回 **requests.Response** 对象。
```python
response = requests.get(url)
# http响应状态码
print(response.status_code)
# http响应文本对应状态码
print(response.reason)
# http响应头
print(response.headers)
# http响应的最终URL
print(response.url)
# 调用 response.text 时解码字符类型
print(response.encoding)
# 获取 cookies
print(response.cookies)
# 响应内容以 unicode 表示
print(response.text)
# 将响应内容格式化为 JSON
print(response.json())
# 响应内容以字节表示
print(response.content)
```

### 总结
requests 的使用确实如同官方文档所讲的那样简单，在使用上不必过多关注于请求内部的实现，只需将重心放在**请求路径、请求参数、请求头、响应体**上，其他的操作都在 requests 的内部实现。

以上介绍 requests 简单的请求，已经足够应用在 ”爬虫“ 中了。更多的复杂请求请查看[Requests文档](https://requests.readthedocs.io/en/master/) 。
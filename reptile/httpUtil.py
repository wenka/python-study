import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
}


class Request:

    def __init__(self, url):
        self.url = url

    def get_response(self):
        resp = requests.get(self.url,headers = headers)
        return resp.text

    def get_response_json(self):
        resp = requests.get(self.url,headers = headers)
        return resp.json()


if __name__ == '__main__':
    url = 'https://blog.csdn.net/wenka'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
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
    # print(response.json())
    # 响应内容以字节表示
    print(response.content)

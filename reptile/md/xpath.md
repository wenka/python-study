## 解析网页内容，获取数据信息

> 前一篇讲解如何获取网页资源，先如今的问题为如何拿取网页中的数据信息？

分为一下步骤：
1. 定位目标数据
2. 检查目标数据的节点信息
3. 生成 xpath 路径信息
4. 使用 **etree** 库，通过 **xpath** 解析出目标数据

## 1. 前提准备

### 1.1 技能准备

1. [python 语法](https://www.runoob.com/python3/python3-tutorial.html)
2. [一种 http python 请求工具](https://blog.csdn.net/wenka_/article/details/106570160)
3. [XPATH语法](https://www.runoob.com/xpath/xpath-tutorial.html)

### 1.2 python环境类库导入：
```python
# 实现扩展了ElementTree API
from lxml import etree
# HTML and XHTML 解析其 
from html.parser import HTMLParser
```

### 1.3 定位目标数据资源：

本文以爬取 CSDN 个人文章为例，链接地址： [menglinjie的博客](https://blog.csdn.net/menglinjie) 。
为啥要爬这位大佬的文章呢，给个表情自行体会。

![傲娇](https://img-blog.csdnimg.cn/20200609135404692.jpg#pic_center)

## 2. 代码编写
我们先解读一下所要爬取的网页内容：
![网页内容](https://img-blog.csdnimg.cn/20200609134309511.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlbmthXw==,size_16,color_FFFFFF,t_70#pic_center)

---

中间的列表项就是我们所要爬取的文章列表
- 红色框是单个文章体
    - 蓝色框是文章标题
    - 红色框是文章摘要
    - 绿色框从左到右分别是创建日期，查阅数量，评论数量

鼠标右键检查数据的DOM元素
![F12](https://img-blog.csdnimg.cn/20200609140000108.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlbmthXw==,size_16,color_FFFFFF,t_70#pic_center)

- div[class='article-list'] 即为文章的列表父标签
- 子节点带有 data-articleid 属性的 DIV 即为文章体
    - 序号①：data-articleid属性为文章Id
    - 序号②：文章内容的 URL
    - 序号③：文章标题
    - 序号④：文章摘要
    - 序号⑤：创建日期
    - 序号⑥：查阅次数
    - 序号⑦：评论数量
So:
### 2.1 定义文章的实体类
```python
class Article:
    """
    文章
    """

    def __init__(self):
        self.id = '' # 文章ID
        self.url = '' # 文章的链接
        self.title = '' # 文章标题
        self.create_time = '' # 创建时间
        self.summary = '' # 摘要
        self.read_num = 0 # 查阅数量
        self.comment_num = 0 # 评论数量
        self.content = '' # 文章内容

    def __repr__(self):
        return '<Article(id=%s,title=%s,create_time=%s,read_num=%s,comment_num=%s,url=%s)>' % (
            self.id, self.title, self.create_time, self.read_num, self.comment_num, self.url)
```
### 2.2 解析数据
先上代码：

```python

if __name__ == '__main__':
    # 文件的 xpath 解读：取任意位置下 class="article-list" 的div节点下带有 data-articleid 属性的div节点。
    article_xpath = '//div[@class="article-list"]/div[@data-articleid]'
    url = 'https://blog.csdn.net/menglinjie'
    # httpUtil 为上一节写的 http 请求类
    response_html = httpUtil.Request(url=url).get_response()
    html = etree.HTML(response_html)
    articles = html.xpath(article_xpath)
    for article_element in articles:
        article = Article()
        # 文章Id 【el.get(string) 获取属性】
        article.id = article_element.get('data-articleid')
        # 文章内容路径 【查询相对路径 h4节点下的a节点的 href 属性】
        article.url = article_element.find('h4/a').get('href')
        # 文章标题  【查询相对路径 h4节点下的a节点的文本信息，strip()去除前后空格】
        article.title = article_element.find('h4/a/').tail.strip()
        # 文章创建时间 【查询相对路径 div节点下p节点下class=date的span节点的内容数据，strip()去除前后空格】
        article.create_time = article_element.find('div/p/span[@class="date"]').text.strip()
        # 摘要  【查询相对路径 class=content的p节点的内容数据，strip()去除前后空格】
        article.summary = article_element.find('p[@class="content"]/a').text.strip()
        # 查阅数量 【查询相对路径 div下的p节点下的第2个span下的img标签的文本信息，strip()去除前后空格】
        article.read_num = article_element.find('div/p/span[2]/img').tail.strip()
        # 评论数量 【查询相对路径 div下的p节点下的第3个span下的img标签的文本信息，strip()去除前后空格】
        article.comment_num = article_element.find('div/p/span[3]/img').tail.strip()
        # 通过文章URL　获取文章内容
        content_response_html = httpUtil.Request(url=article.url).get_response()
        # 匹配id="article_content"的内容，解析返回根节点对象
        content_el = etree.HTML(content_response_html).xpath('//*[@id="article_content"]')[0]
        # 格式化为HTML字符串
        content = HTMLParser().unescape(etree.tostring(content_el, method='html').decode())
        article.content = content
        print(article)
```

说明：
   > response_html：即http请求返回的内容

   > etree.HTML(html:string)：从字符串常量解析HTML文档,返回其根节点对象。

   > *.xpath(xpath:string)：通过xpath获取该根节点下匹配的 element 节点对象

## 3. 补充

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;其实，最主要的一点就是确定目标的XPath信息，以及资源的路径信息。上述示例中只简述了获取当前页面的文章信息，其实并不全面。若想获取该博主的全部文章信息，需先解析当前页面的文章分页信息，
然后，根据其分页路径，逐个解析每个页面的文章，方能拿到该博主的全部文章信息。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;同时，该页面的有用信息不单单文章列表，亦有博主的博客统计信息、文章分类信息、文章归档信息、评论数据信息等。

--- 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;若有不熟悉XPATH的小伙伴，可通过 F12 查询目标的DOM元素，**右键 -> _Copy_ -> _Copy XPath_(或者 *Copy full XPath* )** 获取其Xpath路径信息。
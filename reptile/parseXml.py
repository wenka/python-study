from reptile import httpUtil
from lxml import etree
from html.parser import HTMLParser

article_xpath = '//div[@class="article-list"]/div[@data-articleid]'


class Article:
    """
    文章
    """

    def __init__(self):
        self.id = ''
        self.url = ''
        self.title = ''
        self.create_time = ''
        self.summary = ''
        self.read_num = 0
        self.comment_num = 0
        self.content = ''

    def __repr__(self):
        return '<Article(id=%s,title=%s,create_time=%s,read_num=%s,comment_num=%s,url=%s)>' % (
            self.id, self.title, self.create_time, self.read_num, self.comment_num, self.url)


if __name__ == '__main__':
    url = 'https://blog.csdn.net/menglinjie'
    response_html = httpUtil.Request(url=url).get_response()
    html = etree.HTML(response_html)
    articles = html.xpath(article_xpath)
    for article_element in articles:
        article = Article()
        # 文章Id
        article.id = article_element.get('data-articleid')
        # 文章内容路径
        article.url = article_element.find('h4/a').get('href')
        # 文章标题
        article.title = article_element.find('h4/a/').tail.strip()
        # 文章创建时间
        article.create_time = article_element.find('div/p/span[@class="date"]').text.strip()
        # 摘要
        article.summary = article_element.find('p[@class="content"]/a').text.strip()
        # 查阅数量
        article.read_num = article_element.find('div/p/span[2]/img').tail.strip()
        # 评论数量
        article.comment_num = article_element.find('div/p/span[3]/img').tail.strip()
        # 通过文章URL　获取文章内容
        content_response_html = httpUtil.Request(url=article.url).get_response()
        content_el = etree.HTML(content_response_html).xpath('//*[@id="article_content"]')[0]
        # 格式化为HTML内容
        content = HTMLParser().unescape(etree.tostring(content_el, method='html').decode())
        article.content = content
        print(article)

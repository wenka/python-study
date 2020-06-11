from html import unescape
from lxml import etree
import execjs
from reptile import httpUtil

article_xpath = '//div[@class="article-list"]/div[@data-articleid]'
path_xpath = '//script'

blog_name = 'menglinjie'


class PageInfo:

    def __init__(self, total, page_size=40):
        self.page_no = 0
        self.total = total
        self.page_size = page_size
        # 计算总页数
        if total % page_size > 0:
            self.total_page = total // page_size + 1
        else:
            self.total_page = total // page_size

    def has_next(self):
        return self.page_no < self.total_page

    def next_page(self):
        self.page_no = self.page_no + 1
        return self.page_no

    def __repr__(self):
        return "<PageInfo(current_page:%s, total_page:%s, total:%s, page_size:%s)>" % (
            self.page_no + 1, self.total_page, self.total, self.page_size)


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


def get_page_url(current_page):
    """
    获取分页Url
    :param current_page:
    :return:
    """
    page_url = 'https://blog.csdn.net/%s/article/list/' % (blog_name)
    return page_url + str(current_page)


def get_page_info(blog_url):
    """
    获取分页信息
    :param blog_url:
    :return:
    """
    response_html = httpUtil.Request(url=blog_url).get_response()
    html = etree.HTML(response_html)
    path_html = html.xpath(path_xpath)
    if len(path_html) == 0:
        print('无分页信息！')
        return
    for script in path_html:
        if script.text is not None and 'listTotal' in script.text:
            execjs.compile(script.text)
            get_total_script = '''
            function getTotalCount(){
                return listTotal;
            }
            function getCurrentPage(){
                return currentPage;
            }
            function getPageSize(){
                return pageSize ;
            }
            '''
            execjs_compile = execjs.compile(script.text + get_total_script)
            list_total = execjs_compile.call('getTotalCount')
            page_size = execjs_compile.call('getPageSize')
            print('总文章数量：', list_total)
            print('分页大小：', page_size)
            return PageInfo(page_size=page_size, total=list_total)


def get_data(page_blog_url):
    """
     通过 CSDN 播客主页地址 获取该博主的博客内容
    :param page_blog_url:  CSDN 播客分页地址
    :return: 文章列表
    """
    response_html = httpUtil.Request(url=page_blog_url).get_response()
    html = etree.HTML(response_html)
    articles = html.xpath(article_xpath)
    # Article 文章对象列表
    article_list = []
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
        content = unescape(etree.tostring(content_el, method='html').decode())
        article.content = content
        article_list.append(article)

    print('%s 总共获取文章【%s】篇。' % (page_blog_url, len(article_list)))
    return article_list


if __name__ == '__main__':
    url = 'https://blog.csdn.net/' + blog_name
    page_info = get_page_info(url)
    articles = []
    while page_info.has_next():
        page = page_info.next_page()
        page_url = get_page_url(page)
        article_list = get_data(page_blog_url=page_url)
        articles.extend(article_list)

    print('总共获取文章【%s】篇。' % len(articles))

    for a in articles:
        print(a)

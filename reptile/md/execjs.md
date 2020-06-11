## 解析执行 JS 脚本代码，获取数据信息

> [前一篇](https://blog.csdn.net/wenka_/article/details/106587678) 讲解了如何使用 **XPath** 解析 _HTML_ 的 _DOM_ 元素。要想拿到全部的博客文章，前提是拿取到页面的分页信息；如今面临的问题是如何获取博客的*分页信息*？？？

通过浏览器 F12 -> Network 中查看我们的爬取的页面 'https://blog.csdn.net/menglinjie' 返回的信息，发现其中并没有页码信息，如下图所示，
```html
<div class="pagination-box" id="pageBox"></div>
```
此DIV标签内没有任务东西，可得出结论：页面所呈现的**分页信息是由JS代码动态渲染上的**。
![F12 URL响应](https://img-blog.csdnimg.cn/20200611133944276.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlbmthXw==,size_16,color_FFFFFF,t_70#pic_center)
通过继续查询该URL的响应信息，不难发现存在一段这样的代码：
![分页脚本信息](https://img-blog.csdnimg.cn/20200611134908446.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlbmthXw==,size_16,color_FFFFFF,t_70#pic_center)
很明显是该博主博客的分页数据：
```javascript
    var currentPage = 1; // 当前页码 
    var baseUrl = 'https://blog.csdn.net/menglinjie/article/list' ; // 分页查询URL
    var pageSize = 40 ; // 分页大小
    var listTotal = 127 ; // 博客文章总数
    var pageQueryStr = ''; // 查询参数
    /**
    * 获取完整的分页查询URL
    */
    function getAllUrl(page) {
        return baseUrl + "/" + page + pageQueryStr;
    }
```
分页信息已经呈现我们面前，但是此处已经不能通过Xpath解析了，摆在面前的首要问题就是如何解析JS脚本？

So:

这里需要引入一个可以调用 JS 脚本的 Python 库： **PyExecJS**

## 1. 引入 **PyExecJS**

### 1.1 项目导入PyExecJS
命令执行
```shell script
pin install PyExecJS
```
代码导入该模块：
```python
import execjs
```

### 1.2 PyExecJS使用介绍
查看模块下 __init\__.py 源码：
```python
.....

register = execjs._runtimes.register
get = execjs._runtimes.get
runtimes = execjs._runtimes.runtimes
get_from_environment = execjs._runtimes.get_from_environment


def eval(source, cwd=None):
    return get().eval(source, cwd)
eval.__doc__ = AbstractRuntime.eval.__doc__


def exec_(source, cwd=None):
    return get().exec_(source, cwd)
exec_.__doc__ = AbstractRuntime.exec_.__doc__


def compile(source, cwd=None):
    return get().compile(source, cwd)
compile.__doc__ = AbstractRuntime.compile.__doc__

```
提供了三个方法：eval,  exec_,  compile
- exec_: 通过JS运行环境执行JS源代码并将输出值作为 String字符串返回
    - print(execjs.exec_('return 1')) # 1
    - print(execjs.exec_('1 + 1')) # None
- eval: 在JS运行环境执行JS表达式
    - print(execjs.eval('return 1')) # 报错
    - print(execjs.eval('1 + 1')) # 2
- compile: 作为上下文对象的源。源代码可用于执行其他代码

## 2. 应用
再回顾一下我们需要解析的 JS 代码：
```javascript
    var currentPage = 1; // 当前页码 
    var baseUrl = 'https://blog.csdn.net/menglinjie/article/list' ; // 分页查询URL
    var pageSize = 40 ; // 分页大小
    var listTotal = 127 ; // 博客文章总数
    var pageQueryStr = ''; // 查询参数
    /**
    * 获取完整的分页查询URL
    */
    function getAllUrl(page) {
        return baseUrl + "/" + page + pageQueryStr;
    }
```
我们需要的数据：
- pageSize： 分页大小
- listTotal：博客总数

由此两值即可计算出分页情况。

所以：

第一步：先编写我们的JS片段
```javascript
// 获取总数
function getTotalCount(){
    return listTotal;
}
// 获取分页大小
function getPageSize(){
    return pageSize ;
}
```

第二步：与源JS代码一起编译进上下文
```python
# script变量为源JS代码
# custom_script变量为上述自定义的JS片段
execjs_compile = execjs.compile(str(script) + custom_script)
```
第三步：执行JS脚本，获取方法返回值
execjs.compile 返回 ExternalRuntime.Context 对象，其拥有 _def call(self, fn, *args, **kwargs)_ 方法
> fn: 方法名
> args：方法参数
```python
# 执行 getTotalCount 方法
list_total = execjs_compile.call('getTotalCount')
# 执行 getPageSize 方法
page_size = execjs_compile.call('getPageSize')
```

## 3. 总结

完整python代码：
```python
# 通过 xpath 获取 html中 script 标签内容
path_xpath = '//script/text()'
response_html = httpUtil.Request(url=blog_url).get_response()
html = etree.HTML(response_html)
# 解析得到所有的 script 脚本内容
path_html = html.xpath(path_xpath)
if len(path_html) == 0:
    print('无分页信息！')
    return
for script in path_html:
    # 遍历找到含有分页信息的脚本片段
    if 'listTotal' in str(script):
        # 自定义脚本
        custom_script = '''
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
        # 编译JS代码加入JS运行环境上下文
        execjs_compile = execjs.compile(str(script) + custom_script)
        # 执行JS方法，获取分页信息
        list_total = execjs_compile.call('getTotalCount')
        page_size = execjs_compile.call('getPageSize')
        print('总文章数量：', list_total)
        print('分页大小：', page_size)
```

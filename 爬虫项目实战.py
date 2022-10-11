目的
https://shareae.com/after-effects-project
根据要求指定爬虫计划
1.图片不能有水印
    无法控制 只能根据特定的接口(无水印的图片链接)

2.图片视频保存要以该主题(图片)的id文件名保存  132456.jpg
满足条件 实现 对链接进行切割  取到id 作为文件名字符串

3.图片视频保存到不同的文件夹
保存的时候指定路径  图片dir/视频dir

4可以自己指定爬取的页数
先爬取一页的数据   再爬取多页的数据   从 10  20  需要根据用户的输入改变起始url  以及结束的url
https://shareae.com/after-effects-project/page/1/
第二页
https://shareae.com/after-effects-project/page/2/
第三页
https://shareae.com/after-effects-project/page/3/
第四页
https://shareae.com/after-effects-project/page/4/
  import re
import requests
from lxml import etree
class spiderss():
    def __init__(self):
        self.headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "cookie": "_ga=GA1.2.1292249770.1648125313; _gid=GA1.2.1006201103.1656675603; PHPSESSID=qc3vl9ub5592d6g538s3doaci2; _gat=1"
        }
    # 向一级目录发送请求的方法
    # 翻页使用params参数时要注意 url的参数必须是xxx=xxx  这种类型才能通过params 传参 ，否则uel拼接
    def first_spider(self,i):
        self.url=f"https://shareae.com/after-effects-project/page/{i}/"
        first_response=requests.get(url=self.url,headers=self.headers)
        first_data=first_response.content.decode()
    #     数据类型转换 str >>element
        html1=etree.HTML(first_data)
    #     清洗出整页的二级目录url 50个
        second_urls=html1.xpath('//div[@id="dle-content"]/div/h2/a/@href')
        # print(second_urls)
        print(len(second_urls))
        print("正在请求二级目录url")
        # 传递50个 url列表
        self.second_spider(second_urls)
    # 向二级目录发送请求的方法
    def second_spider(self,second_urls):
        # 循环列表 发送请求
        for second_url in second_urls[1:2]:
            response2=requests.get(url=second_url,headers=self.headers)
            data=response2.text
            # html2=etree.HTML(data)
            # third_url=html2.xpath('//div[@class="buttondownload1"]/a/@href')
            # xpath提取失效  正则 href="https://videohive.net/item/essential-text-animation-presets/37955735"
            # 根据url的唯一性参数作为正则表达式 进行url匹配  思路
            # href="(.*?)" 视情况使用
            third_url=re.findall('href="(https://videohive.net/item/essential-text-animation-presets/\d*)"',data)[0]
            print(third_url)
            self.third_spider(third_url)
    # 向三级目录发送请求的方法
    def third_spider(self,third_url):
        #  三级目录url https://videohive.net/item/urban-outfit-slideshow/37715043
        id=third_url.split("/")[-1]
        print("正在爬取三级目录")
        response3=requests.get(url=third_url,headers=self.headers)
        data3=response3.content.decode()
        print(data3)
        video_url=re.findall('href="(https://previews.customer.envatousercontent.com/h264-video-previews/.*?/\d*.mp4)"',data3)[0]
        print(video_url)
        photourl=re.findall('width="\d*" height="\d*" src="(.*?)"',data3)[0]
        photourl=photourl.replace("amp:","")
        print(photourl)
        self.save_media(video_url,photourl,id)
    # 向视频图片url发送请求的方法
    def save_media(self,video_url,photourl,id):
        # 保存视频的请求
        videores=requests.get(url=video_url,headers=self.headers)
        with open(f"D:/B站爬虫视频/{id}.mp4","wb")as file1:
            file1.write(videores.content)
            print("视频保存成功")
        # 保存图片的请求 爬取图片会出现 响应慢  报错  完善  通过timeout参数结合while True配合发送请求
        # 会报 连接超时错误 计算机远程连接失败
        photores=requests.get(url=photourl,headers=self.headers)
        with open(fr"D:\Download\B站视频爬取\图片\{id}.jpg",mode="wb")as file2:
            file2.write(photores.content)
            print("图片保存成功")

    def run(self):
        # 需要指定范围    可以 指定10>>20   30>>40
        start_num=int(input("请输入起始的页数:"))
        end_num=int(input("请输入结束的页数:"))
        for i in range(start_num,end_num+1):
            self.first_spider(i)

if __name__ == '__main__':
    spider=spiderss()
    spider.run()

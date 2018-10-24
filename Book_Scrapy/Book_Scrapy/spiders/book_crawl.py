
import scrapy
import pymongo
import re
from Book_Scrapy.items import BookScrapyItem

pageSequence_1 = 1
url_break=[] # 没有章节的书。
item=BookScrapyItem()
class book_crawl(scrapy.Spider):

    name = 'book_crawl'

    start_urls = ['https://www.booktxt.net/xiaoshuodaquan/']

    def parse(self, response):
        global pageSequence_1
        pageSequence_1=pageSequence_1+1
        novellist = response.css('#main li')
        self.logger.info(' 总共有多少本书：%s ', len(novellist))
        self.logger.info('第一层的网址： %s；pageSequence_1 ：%s', response.url,str(pageSequence_1))
        for novel in novellist:
            # print('第一层>pageSequence_1: ' + str(pageSequence_1))
            href = novel.css('a::attr(href)').extract_first()
            if href in url_break:
                break
            # print('pageSequence_1:'+pageSequence_1)
            #print('book_name: '+book_name +'href: '+href)
            yield scrapy.Request(url=href,callback=self.parse_chapter)

    def parse_chapter(self,response):
        global pageSequence_1
        pageSequence_1 = pageSequence_1 + 1
        self.logger.info('第二层的网址： %s；pageSequence_1 ：%s', response.url, str(pageSequence_1))
        # print('第二层>pageSequence_1:' + str(pageSequence_1))

        # book_type =response.css('.con_top::text').extract()
        # print(book_type)
        # book_type_1=re.findall(r"(?=<a href="//">顶点小说</a>).*(?=最新章节)", book_type)
        url_sencond = response.css('#list a::attr(href)').extract_first()
        if url_sencond is None:
            url_break.append(response.url)
            self.logger.info('这本书是费书，网址是：%s', response.url)
            yield scrapy.Request(url='https://www.booktxt.net/xiaoshuodaquan/', callback=self.parse_chapter_detail)

        item['book_name'] = response.css('#info h1::text').extract()[0]
        item['book_author']=response.css('#info p::text').extract()[0]
        item['last_update_time']=response.css('#info p::text').extract()[4].replace('最后更新：','')
        item['book_introduce']=response.css('#intro p::text').extract()[0]

        href_chapter=response.url+url_sencond
        yield scrapy.Request(url=href_chapter, callback=self.parse_chapter_detail)
        # print('book_type: '+book_type_1)
        # print('book_author: '+book_author)
        # print('last_update_time: '+last_update_time)
        # print(book_introduce)
        # print(href_chapter)

    def parse_chapter_detail(self,response):
        global pageSequence_1
        pageSequence_1 = pageSequence_1 + 1
        self.logger.info('第三层的网址： %s；pageSequence_1 ：%s', response.url, str(pageSequence_1))
        # print('第三层>pageSequence_1: ' + str(pageSequence_1))
        # if pageSequence_1>500:
        #     self.crawler.engine.close_spider(self, '在这里结合苏吧')
        item['book_chapter'] = response.css('.bookname h1::text').extract()[0]
        item['book_content'] = response.css('#content::text').extract()
        item['book_id']=response.css('.bottem2 a::attr(href)').extract()[2]
        item['book_content_url']=response.url
        book_chapter_first= response.css('.bottem2 a::attr(href)').extract()[1]
        book_chapter_mulu = response.css('.bottem2 a::attr(href)').extract()[2]
        book_chapter_end= response.css('.bottem2 a::attr(href)').extract()[3]

        # href_chapter_after='https://www.booktxt.net'+book_chapter_mulu+book_chapter_end    #下一章
        yield  item
        if book_chapter_first !='index.html':
            href_chapter_before = 'https://www.booktxt.net' + book_chapter_mulu + book_chapter_first  # 上一章
            yield scrapy.Request(url=href_chapter_before, callback=self.parse_chapter_detail)
        # 如果最后一章，book_chapter_ater='index.html'
        # 如果第一章,book_chapter_before='index.html'
        # global pageSequence
        # if(book_chapter_first=='index.html' and book_chapter_end!='index.html'):# 如果是本章是第一章，且不是最后一章。
        #     yield scrapy.Request(url=href_chapter_after, callback=self.parse_chapter_detail)
        # elif(book_chapter_first=='index.html' and book_chapter_end=='index.html'):# 如果本章是第一章，同时也是最后一章，就有问题了。
        #     exit('soryy')
        # elif(book_chapter_first!='index.html' and book_chapter_end=='index.html'):# 如果本章是最后一张，就可以抓取下一个了。
        #     exit('soory')
        # else:
        #     yield scrapy.Request(url=href_chapter_before, callback=self.parse_chapter_detail)






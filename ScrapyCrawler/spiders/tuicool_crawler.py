# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from ScrapyCrawler.items import TuicoolItem

class TuicoolCrawlerSpider(CrawlSpider):
    name = 'tuicool_crawler'
    allowed_domains = ['tuicool.com']
    start_urls = ['http://www.tuicool.com/ah/20/0?lang=1']

    rules = (
        Rule(LinkExtractor(allow=r'ah/20/[0-20]\?lang=1'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        articles = response.xpath('//*[@id="list_article"]/div')

        for article in articles:
            item = TuicoolItem()
            item['imageUrl'] = article.xpath('./div/img/@src').extract()[0].strip()
            item['articleTitle'] = article.xpath('./div/div/a/text()').extract()[0].strip()
            item['articleUrl'] = 'http://www.tuicool.com%s' % article.xpath('./div/div/a/@href').extract()[0].strip()
            item['articleSourceName'] = article.xpath('./div/div/span[1]/text()[normalize-space()]').extract()[0].strip()
            item['publishDateTime'] = article.xpath('./div/div/span[3]/text()').extract()[0].strip()
            articalPage = scrapy.Request(item['articleUrl'], 
                                        callback=self.parse_page_content,
                                        errback=self.errorback,
                                        dont_filter=True)
            articalPage.meta['item'] = item
            yield articalPage

    def parse_page_content(self, response):
        item = response.meta['item']
        sourceUrls =  response.xpath('//*[@class="article_meta"]/div[@class="source"]/a/@href').extract()
        if len(sourceUrls) < 1:
            # deal with pages from zhuanlan.zhihu.com, it seems not work, to do
            item['articleSourceUrl'] = response.url
            item['articleContent'] = ''.join(response.xpath('//*[@id="react-root"]/div/div/div[3]/div[2]/descendant::text()').extract())
        else:
            item['articleSourceUrl'] = sourceUrls[0].strip()
            item['articleContent'] = ''.join(response.xpath('//*[@id="nei"]/descendant::text()').extract())
        yield item

    def errorback(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

import scrapy
from scrapy.spiders import SitemapSpider
from datetime import datetime

# class AluthCrawl(scrapy.Spider):
class BaiscopeCrawl(SitemapSpider):
    name = "baiscope_crawl"

    sitemap_urls = ['https://www.baiscopelk.com/sitemap.xml']
    sitemap_follow = ["^.*https://www.baiscopelk.com/sitemap-pt-post-.*$"]
    sitemap_rules = [('^.*-sinhala-subtitles/.*$', 'parse')]
    count = 0
    #

    def sitemap_filter(self, entries):
        for entry in entries:
            date_time = datetime.strptime(entry['lastmod'][:-6], '%Y-%m-%dT%H:%M:%S')
            if date_time.year == 2019:
                print(date_time)
                yield entry

    def parse(self, response):
        for element in response.xpath('//div[@class="post-inner"]'):
            self.count+=1
            englishTitle = element.xpath('./h1[@class="name post-title entry-title"]/span/text()').get().split('|')[0]
            sinhalaTitle = element.xpath('./h1[@class="name post-title entry-title"]/span/text()').get().split('|')[1]

            relevantStatus = ''
            status =element.xpath('//*[@id="the-post"]/div/p/span[2]/a/text()').getall()
            for state in status:
                if (state != 'All' and state != 'Featured Articles' and state != 'Sinhala Subtitle'):
                    relevantStatus += state+','

            views = (element.xpath('./p[@class="post-meta"]/span/text()').getall()[-1]).split(' ')[0].strip(' ')
            newViews =''
            for digit in views:
                if(digit != ',' ):
                    newViews+=digit

            noOfComments = element.xpath('//*[@id="the-post"]/div/p/span[3]/a/text()').get().split(' ')[0].strip(' ')
            newNoOfComments = ''
            for digit in noOfComments:
                if(digit != ','):
                    newNoOfComments+=digit

            content = element.xpath('./div[@class="entry"]/p/span/text()').getall()
            filtered_content = element.xpath('./div[@class="entry"]/p/span/text()').getall()[:len(content)-4]
            subtitle_description = ''
            for para in filtered_content:
                subtitle_description += para.strip("\n")

            yield {
                'id': self.count,
                'englishTitle': englishTitle.strip(),
                'sinhalaTitle': sinhalaTitle.strip(),
                'date': element.xpath('./p[@class="post-meta"]/span/text()').getall()[0],
                'views': int(newViews),
                'noOfComments': int(newNoOfComments),
                'status': relevantStatus,
                'content': subtitle_description.strip(),
            }


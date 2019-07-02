import scrapy
from scrapy.spiders import SitemapSpider
from datetime import datetime

# class AluthCrawl(scrapy.Spider):
class BaiscopeCrawl(SitemapSpider):
    name = "baiscope_crawl"

    sitemap_urls = ['https://www.baiscopelk.com/sitemap.xml']
    sitemap_follow = ["^.*https://www.baiscopelk.com/sitemap-pt-post-.*$"]
    sitemap_rules = [('^.*-sinhala-subtitles/.*$', 'parse')]

    #

    def sitemap_filter(self, entries):
        for entry in entries:
            date_time = datetime.strptime(entry['lastmod'][:-6], '%Y-%m-%dT%H:%M:%S')
            if date_time.year == 2019:
                print(date_time)
                yield entry

    def parse(self, response):
        for element in response.xpath('//div[@class="post-inner"]'):

            englishTitle = element.xpath('./h1[@class="name post-title entry-title"]/span/text()').get().split('|')[0]
            sinhalaTitle = element.xpath('./h1[@class="name post-title entry-title"]/span/text()').get().split('|')[1]

            relevantStatus = ''
            status =element.xpath('//*[@id="the-post"]/div/p/span[2]/a/text()').getall()
            for state in status:
                if (state != 'All' and state != 'Featured Articles' and state != 'Sinhala Subtitle'):
                    relevantStatus += state+','

            content = element.xpath('./div[@class="entry"]/p/span/text()').getall()
            filtered_content = element.xpath('./div[@class="entry"]/p/span/text()').getall()[:len(content)-4]
            subtitle_description = ''
            for para in filtered_content:
                subtitle_description += para.strip("\n")

            yield {
                'englishTitle': englishTitle,
                'sinhalaTitle': sinhalaTitle,
                'date': element.xpath('./p[@class="post-meta"]/span/text()').getall()[0],
                'views': element.xpath('./p[@class="post-meta"]/span/text()').getall()[-1],
                'noOfComments': element.xpath('//*[@id="the-post"]/div/p/span[3]/a/text()').get(),
                'status': relevantStatus,
                'content': subtitle_description,
            }


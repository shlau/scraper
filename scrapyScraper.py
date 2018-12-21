import scrapy
from scrapy.http import Request

base = 'https://www.greatschools.org'
def normalize_whitespace(str):
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

class SchoolItem(scrapy.Item):  
    name = scrapy.Field()
    link = scrapy.Field()
    county = scrapy.Field()
    city = scrapy.Field()
    phone = scrapy.Field()
    num_schools = scrapy.Field()
    # grades = scrapy.Field()

class SchoolSpider(scrapy.Spider):
    name="schools"
    start_urls = ['https://www.greatschools.org/schools/districts/California/CA/']

    def parse(self,response):
        for school in response.css('tr'):
            item = SchoolItem()
            item['name'] = school.css('a::text').extract()
            item['city'] = normalize_whitespace(u''.join(school.css('td:nth-child(2)::text').extract()))
            item['county'] = normalize_whitespace(u''.join(school.css('td:last-child::text').extract()))
            # item['link'] = base + str(u''.join(school.css('a::attr(href)').extract()))
            link = base + str(u''.join(school.css('a::attr(href)').extract()))
            if link:
                yield Request(url=link, callback=self.parse_page2, meta={'item': item})

    def parse_page2(self,response):
        school_info = response.css('.district-hero-stats > div > div:last-child::text')
        item = response.meta['item']
        item['phone'] = '555-5555'
        num_schools = school_info
        # grades = school_info[1].text.strip()
        item['num_schools'] = num_schools
        # item['grades'] = grades
        yield item
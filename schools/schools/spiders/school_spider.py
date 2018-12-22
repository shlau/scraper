import scrapy
from scrapy.http import Request
from schools.items import SchoolsItem
import scrapy_splash
base = 'https://www.greatschools.org'
def normalize_whitespace(str):
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

class SchoolSpider(scrapy.Spider):
    name="schools"
    start_urls = ['https://www.greatschools.org/schools/districts/California/CA/']

    def parse(self,response):
        schools = response.css('tr')
        if schools:
            for school in schools:
                item = SchoolsItem()
                item['name'] = str(u''.join(school.css('a::text').extract()))
                item['city'] = normalize_whitespace(u''.join(school.css('td:nth-child(2)::text').extract()))
                item['county'] = normalize_whitespace(u''.join(school.css('td:last-child::text').extract()))
                link = base + str(u''.join(school.css('a::attr(href)').extract()))
                if link:
                    yield scrapy_splash.SplashRequest(url=link, callback=self.parse_page2, meta={'item': item}, endpoint='render.html')
        else:
            return

    def parse_page2(self,response):
        item = response.meta['item']
        num_schools = normalize_whitespace(u''.join(response.css('.district-hero-stats > div > div:last-child::text').extract()[0]))
        grades = normalize_whitespace(u''.join(response.css('.district-hero-stats > div > div:last-child::text').extract()[1]))
        phone = normalize_whitespace(u''.join(response.css('.badge-and-content span.content::text').extract()))
        school_url = normalize_whitespace(u''.join(response.css('a.content::attr(href)').extract()))
        item['phone'] = phone
        item['grades'] = grades
        item['num_schools'] = num_schools
        item['website'] = school_url
        # item['grades'] = grades
        yield item
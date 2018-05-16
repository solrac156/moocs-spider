# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import urlparse
import scrapy
from scrapy.http import Request
from functools import partial
from moocs.items import MoocsItem
import re

class MoocsSpiderSpider(scrapy.Spider):
    name = "moocs_spider"
    start_urls = ['https://www.coursetalk.com/subjects/data-science/courses']

    def parse(self, response):
        xpath_courses_links = '//*[@class="link-unstyled js-course-search-result"]//a/@href'
        courses_relative_links = response.xpath(xpath_courses_links).re('.+/courses/.+')
        courses_links = [urlparse.urljoin(response.url, courses_relative_url) for courses_relative_url in
                         courses_relative_links]
        for course_link in courses_links:
            yield Request(course_link, callback=partial(self.extract_course_data))
        result_pages = [page for page in response.xpath('//*[@class="pagination"]//@href').extract() if
                        '/courses' in page]
        for page in result_pages:
            yield Request(page, callback=partial(self.parse))

    def extract_course_data(self, response):
        item = MoocsItem()
        usernames = self.extract_user_name(response)
        stars_numbers = self.extract_stars_number(response)
        last_updates = self.extract_last_update(response)
        review_bodys = self.extract_review_body(response)
        course_stages = self.extract_course_stage(response)
        for review in zip(usernames, stars_numbers, last_updates, review_bodys, course_stages):
            item['user_name'] = review[0]
            item['stars_number'] = review[1]
            item['last_update'] = review[2]
            item['review_body'] = review[3]
            item['course_stage'] = review[4]
            yield item

    @staticmethod
    def extract_user_name(response):
        user_name_xpath = '//*[@class="review-body__username"]//text()'
        user_names = response.xpath(user_name_xpath).extract()
        user_names = [username.replace('\n', ' ').replace(',', ' ').replace(';', ' ').strip()
                      for username in user_names]
        return user_names

    @staticmethod
    def extract_stars_number(response):
        stars_number_xpath = '//*[@class="review-body-info"]/span[@class="sr-only"]/text()'
        stars_numbers = response.xpath(stars_number_xpath).extract()
        stars_numbers = [stars.replace(',', ' ').replace(';', ' ').strip() for stars in stars_numbers]
        stars_numbers = [re.search('(\d+|None)/(\d+) stars', stars).group(1) for stars in stars_numbers]
        return stars_numbers

    @staticmethod
    def extract_last_update(response):
        last_update_xpath = '//*[@itemprop="datePublished"]/text()'
        last_updates = response.xpath(last_update_xpath).extract()
        last_updates = [last_update.replace(u'\xa0', ' ').replace(',', ' ').replace(';', ' ').strip()
                        for last_update in last_updates]
        return last_updates

    @staticmethod
    def extract_review_body(response):
        review_body_xpath = '//*[@class="review-body__content"]/span[@class="more-less-trigger__text--full"]/text()'
        review_bodys = response.xpath(review_body_xpath).extract()
        review_bodys = [review_body.replace('\n', ' ').replace('\r', ' ').replace(',', ' ').replace(';', ' ').strip()
                        for review_body in review_bodys]
        return review_bodys

    @staticmethod
    def extract_course_stage(response):
        course_stage_xpath = '//*[@class="review-body-info"]/span[3]/text()'
        course_stages = response.xpath(course_stage_xpath).extract()
        course_stages = [course_stage.replace(',', ' ').replace(';', ' ').strip() for course_stage in course_stages]
        return course_stages


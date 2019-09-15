# -*- coding: utf-8 -*-
import scrapy
import datetime
import dateutil
from dateutil import parser

class ClienSpider(scrapy.Spider):
    name = "clien"

    start_urls = [
        'https://m.clien.net/service/board/jirum?&od=T31&po=0',
    ]

    def parse(self, response):

        now = datetime.datetime.now()
        delta = datetime.timedelta(days=3, seconds=3600)

        results = []


        css_components = {
        "items":".list_item.symph-row",
        "subject":".list_subject",
        "viewer":".list_hit",
        "date":".list_time",
        "comment":".list_reply",
        "like":".list_symph"
        }


        items = response.css(css_components.get("items"))
        for item in items:

            result = {}

            date_element = item.css(css_components.get("date"))
            date_str = item.css(css_components.get("date")).pop().css("span::text").get()
            date_str = date_str.strip()
            date_time = parser.parse(date_str)
            date = date_time.strftime("%Y-%m-%d")

            if now - delta > date_time:
                break

            result['date'] = date

            subject = item.css(css_components.get("subject")).pop()
            title = "".join(subject.css("::text").getall()).strip()

            if subject.css(".solidout"):
                continue;

            result['title'] = title
            href = response.urljoin(subject.attrib['href'])

            viewer_element = item.css(css_components.get("viewer"))

            if viewer_element:
                view = viewer_element.pop().css("span::text").get()
            else:
                view = 0


            comment_element = item.css(css_components.get("comment"))

            if comment_element:
                comment = comment_element.pop().css("span::text").get()
            else:
                comment = 0

            like_element = item.css(css_components.get("like"))
            if like_element:
                like = like_element.pop().css("span::text").get()
            else:
                like = 0

            """
            이하 결과 값 세팅하는 부분        
            """


            result['url'] = href

            if "k" in view:
                view = float(view.split("k")[0])*1000
            elif "m" in view:
                view = float(view.split("m")[0]) * 1000000
            view = int(view)

            result['view'] = view

            comment = int(comment)
            result['comment'] = int(comment)

            like = int(like)
            result['like'] = like

            result['score'] = view * like + comment * 100

            yield result

    def parse_reply(self,response):
        pass
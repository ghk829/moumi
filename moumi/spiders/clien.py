# -*- coding: utf-8 -*-
import scrapy
import datetime
import dateutil
from dateutil import parser
import uuid
from selenium import webdriver

class ClienSpider(scrapy.Spider):
    name = "clien"

    start_urls = [
        'https://m.clien.net/service/board/jirum?&od=T31&po=0',
        'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu'
    ]

    def parse(self, response):

        now = datetime.datetime.now()
        delta = datetime.timedelta(days=3, seconds=3600)

        results = []

        if response.url.startswith("https://m.clien.net"):
            css_components = {
            "items":".list_item.symph-row",
            "subject":".list_subject",
            "viewer":".list_hit",
            "date":".list_time",
            "comment":".list_reply",
            "like":".list_symph"
            }

            yield from self.parse_clien(response, css_components, now, delta)

        elif response.url.startswith("http://www.ppomppu.co.kr"):
            css_components = {
                "items": [".list1",".list0"],
                "subject": ".list_subject",
                "viewer": ".list_hit",
                "date": ".list_time",
                "comment": ".list_reply",
                "like": ".list_symph"
            }

            yield from self.parse_ppom(response, css_components, now, delta)


    def parse_clien(self,response,css_components,now,delta):

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
            result['id'] = "clien_"+str(uuid.uuid4())
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

    def parse_ppom(self,response,css_components,now,delta):
        driver = webdriver.PhantomJS("phantomjs")
        driver.get(response.url)
        driver.explca(3)
        from scrapy import Selector
        selector = Selector(text=driver.page_source)

        items = []
        for css in css_components.get("items"):
            items += selector.css(css)

        for item in items:
            try:
                result = {}
                result['id'] = "ppom_" + str(uuid.uuid4())
                for idx,information in enumerate(item.css("td.list_vspace")):

                    if idx ==0:
                        "아이템 번호"
                    elif idx ==1:
                        "기타"
                    elif idx ==2:
                        "저자"
                    elif idx ==3:
                        "타이틀"
                        "URL"
                        href = response.urljoin(information.css("a")[0].attrib['href'])
                        result['url'] = href
                        comment = ''.join([e.strip() for e in information.css(".list_comment2")[0].css("::text").extract()])
                        comment = int(comment)
                        result['comment'] = comment
                        if information.css(".list_title"):
                            result['title'] = ''.join([e.strip() for e in information.css("::text").extract()])
                        else:
                            continue
                    elif idx ==4:
                        "날짜"
                        date_str = information.css("::text").get().strip()
                        date_time = parser.parse(date_str)
                        date = date_time.strftime("%Y-%m-%d")
                        if now - delta > date_time:
                            break
                        result['date'] = date

                    elif idx ==5:
                        "like"
                        if information.css("::text"):
                            like= information.css("::text").get().split("-")[0]
                            like = int(like)
                        else:
                            like = 0
                        result['like'] = like
                    elif idx ==6:
                        view = information.css("::text").get().strip()
                        view = int(view)
                        result['view'] = view

                result['score'] = view * like + comment * 100

                yield result
            except Exception as e:
                pass
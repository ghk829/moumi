
import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from .moumi.spiders.clien import ClienSpider
from scrapy.utils.project import get_project_settings
settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data.json',
        'FEED_EXPORT_ENCODING': 'utf-8'
}

runner = CrawlerRunner(settings)

def crawl():
    _crawl()
    reactor.run()

@defer.inlineCallbacks
def _crawl():
    runner.join()
    yield runner.crawl(ClienSpider)
    reactor.stop()

def crawl_process():
    def clear_output():
        with open(settings['FEED_URI'], "w") as f:
            try:
                f.write("")
            except Exception as e:
                result = str(e)
    from multiprocessing import Process

    proc = Process(target=crawl)
    proc.start()
    proc.join()
    with open(settings['FEED_URI'],"r") as f:
        try:
            result = f.read()
        except Exception as e:
            result =  str(e)

    if result:
        clear_output();
        return result
    else:
        clear_output();
        return "None"
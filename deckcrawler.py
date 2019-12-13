from crawlers.spiders import DecksSpider
from scrapy.crawler import CrawlerRunner
import sql_helpers
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging


if __name__ == '__main__':

    sql_helpers.create_decks()
    sql_helpers.create_commander()
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        deckID = 0
        yield runner.crawl(DecksSpider, commander='Muldrotha the gravetide', deckID=deckID)
        crs = sql_helpers.sql_connection().cursor()
        deckID = crs.execute("SELECT MAX(deckID) FROM decks").fetchall()[0][0] + 1
        yield runner.crawl(DecksSpider, commander='Scion of the Ur-Dragon', deckID=deckID)
        reactor.stop()

    crawl()
    reactor.run()

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import sql_helpers


class DecksSpider(scrapy.Spider):

    name = "decks"

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        commander = kwargs.get('commander')
        commander.replace(' ', '-').lower()
        self.start_urls = ['https://edhrec.com/listofdecks/%s' % commander]
        self.deckID = kwargs.get('deckID')

    def parse(self, response):

        links = LinkExtractor(restrict_css='div.test_cardlistscontainer').extract_links(response)
        for link in links:
            yield Request(link.url, callback=self.parse_decks_edhrec)

    def parse_decks_edhrec(self, response):
        """
        Takes a single deck link from edhrec and find the tcgplayer buy list to then parse and
        add the deck to the database
        :param response: The response page for the edhrec deck page
        :return: None
        """

        # Splits the cards from one long string to a list of cards from the tcgplayer buy link
        tcg = response.css('div.test_cardlistscontainer a').getall()[1]
        tcg = tcg.split('=')[3].split('&')[0].replace('%20', ' ').replace('%7C%7C', '\n').replace('%2C', ',')\
            .replace('%27', '\'').replace('%2F', '/').replace('1 ', '').replace('%C3%A9', 'é').replace('%C3%BB', 'û')\
            .replace('%C3%B6', 'ö').split('\n')

        con = sql_helpers.sql_connection()
        crs = con.cursor()

        # Insert the commander into the commander table
        commander = tcg.pop(0)
        sql_command = """INSERT INTO commander VALUES ((SELECT name FROM cards WHERE name LIKE '%{}%'), {});""" \
            .format(commander.replace('\'', '\'\''), self.deckID)
        crs.execute(sql_command)
        con.commit()

        # Inserts each card into the decks database
        for item in tcg:
            sql_command = """INSERT INTO decks VALUES ((SELECT name FROM cards WHERE name LIKE '%{}%'), {});"""\
                .format(item.replace('\'', '\'\''), self.deckID)
            crs.execute(sql_command)
        self.deckID = self.deckID + 1
        con.commit()
        con.close()

import scrapy
from ..items import WaterscrapeItem
from ..mongo_provider import MongoProvider
from datetime import datetime
import calendar

class EventsSpider(scrapy.Spider):
    name = "eventSpider"
    allowed_domains = ["internationalrafting.com"]
    start_urls = ["https://www.internationalrafting.com/racing/events/"]
    current_year = ' 2021'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        kwargs["mongo_uri"] = crawler.settings.get("MONGO_URI")
        kwargs["mongo_database"] = crawler.settings.get("MONGO_DATABASE")
        return super(EventsSpider, cls).from_crawler(crawler, *args, **kwargs)

    def __init__(
        self, limit_pages=None, mongo_uri=None, mongo_database=None, *args, **kwargs
    ):
        super(EventsSpider, self).__init__(*args, **kwargs)
        if limit_pages is not None:
            self.limit_pages = int(limit_pages)
        else:
            self.limit_pages = 0
        self.mongo_provider = MongoProvider(mongo_uri, mongo_database)
        self.collection = self.mongo_provider.get_collection()
        # last_items = self.collection.find().sort("published_at", -1).limit(1)
        # self.last_scraped_url = last_items[0]["url"] if last_items.count() else None

    def parse(self, response):

        month_cal = dict((v,k) for v,k in zip(calendar.month_abbr[1:], range(1, 13)))
        self.logger.info(month_cal)

        for post in response.css("div.mec-topsec"):
            self.logger.info('Parse function called on %s', response.url)
            
            ISODate_Start = post.css("span.mec-start-date-label::text").get()
            if ISODate_Start[3] == '-':
                ISODate_Start = ISODate_Start[:2] + ' ' + str(month_cal[ISODate_Start[8:]]) + self.current_year
                self.logger.info(ISODate_Start)
            else:
                ISODate_Start = ISODate_Start[:2] + ' ' + str(month_cal[ISODate_Start[3:6]]) + self.current_year
            ISODate_Start = datetime.strptime(ISODate_Start, '%d %m %Y')
            ISODate_Start.isoformat()

            ISODate_End = post.css("span.mec-end-date-label::text").get()
            if ISODate_End:
                ISODate_End = ISODate_End[3:5] + ' ' + str(month_cal[ISODate_End[6:9]]) + self.current_year
                ISODate_End = datetime.strptime(ISODate_End, '%d %m %Y')
                ISODate_End.isoformat()

            item = WaterscrapeItem(
                dateStart=ISODate_Start,
                dateEnd=ISODate_End,
                description=(
                    post.css("div.mec-event-description::text")
                    .get()
                    .encode("ascii", "ignore")
                    .decode()
                ),
                place=post.css("div.mec-venue-details address span::text").get(),
                url=post.css("a.mec-color-hover::attr('href')").get(),
                name=post.css("a.mec-color-hover::text")
                .get()
                .encode("ascii", "ignore")
                .decode(),
            )

            yield item

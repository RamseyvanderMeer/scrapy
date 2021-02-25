import scrapy
from ..items import WaterscrapeItem
from ..mongo_provider import MongoProvider


class EventsSpider(scrapy.Spider):
    name = "eventSpider"
    allowed_domains = ["internationalrafting.com"]
    start_urls = ["https://www.internationalrafting.com/racing/events/"]

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

        for post in response.css("div.mec-topsec"):
            # self.logger.info('Parse function called on %s', response.url)
            # yield {
            #'title': post.css('a.mec-color-hover::text').get(),
            #'title': post.css('div.mec-event-content h3.mec-event-title a.mec-color-hover::text').get()
            #'date': post.css('span.mec-start-date-label::text').get(),
            #'description': post.css('div.mec-event-description::text').get()
            # }
            item = WaterscrapeItem(
                date=post.css("span.mec-start-date-label::text").get(),
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

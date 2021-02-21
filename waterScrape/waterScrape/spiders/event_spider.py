import scrapy
import json
from waterScrape.items import WaterscrapeItem

class eventsSpider(scrapy.Spider):
    name = "event"

    def start_requests(self):
        urls = [
            'https://www.internationalrafting.com/racing/events/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        events = {}
        
        for post in response.css('div.mec-topsec'):
            #self.logger.info('Parse function called on %s', response.url)
            #yield {
                #'title': post.css('a.mec-color-hover::text').get(),
                #'title': post.css('div.mec-event-content h3.mec-event-title a.mec-color-hover::text').get()
                #'date': post.css('span.mec-start-date-label::text').get(),
                #'description': post.css('div.mec-event-description::text').get()
            #}
            event = {}
            event.update({"date" : post.css('span.mec-start-date-label::text').get(), "description" : post.css('div.mec-event-description::text').get().encode("ascii", "ignore").decode(), "place" : post.css('div.mec-venue-details address span::text').get(), "url" : post.css("a.mec-color-hover::attr('href')").get()})
            events[post.css('a.mec-color-hover::text').get().encode("ascii", "ignore").decode()] = event
            with open('result.json', 'w') as fp:
                json.dump(events, fp)
        
        return events
import scrapy
import json

class eventsSpider(scrapy.Spider):
    name = "event"
    

    start_urls = [
        'https://www.internationalrafting.com/racing/events/'
    ]

    def parse(self, response):
        events = {}
        
        for post in response.css('div.mec-topsec'):
            #yield {
                #'title': post.css('a.mec-color-hover::text').get(),
                #'title': post.css('div.mec-event-content h3.mec-event-title a.mec-color-hover::text').get()
                #'date': post.css('span.mec-start-date-label::text').get(),
                #'description': post.css('div.mec-event-description::text').get()
            #}
            event = {}
            event.update({"date" : post.css('span.mec-start-date-label::text').get(), "description" : post.css('div.mec-event-description::text').get(), "place" : post.css('div.mec-venue-details address span::text').get()})
            events[post.css('a.mec-color-hover::text').get().encode("ascii", "ignore").decode()] = event
            with open('result.json', 'w') as fp:
                json.dump(events, fp)
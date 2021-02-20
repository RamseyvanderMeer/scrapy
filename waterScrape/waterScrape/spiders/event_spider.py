import scrapy
import json

class eventsSpider(scrapy.Spider):
    name = "event"
    

    start_urls = [
        'https://www.internationalrafting.com/racing/events/'
    ]

    def parse(self, response):
        events = {}
        event = {
            "date" : "",
            "description" : ""
        }
        for post in response.css('div.mec-topsec'):
            #yield {
                #'title': post.css('a.mec-color-hover::text').get(),
                #'title': post.css('div.mec-event-content h3.mec-event-title a.mec-color-hover::text').get()
                #'date': post.css('span.mec-start-date-label::text').get(),
                #'description': post.css('div.mec-event-description::text').get()
            #}
            event.update({"date" : post.css('span.mec-start-date-label::text').get(), "description" : post.css('div.mec-event-description::text').get()})
            events[post.css('a.mec-color-hover::text').get()] = event
            with open('result.json', 'w') as fp:
                json.dump(events, fp)
from scrapy.cmdline import execute

try:
    execute(
        [
            "scrapy",
            "crawl",
            "eventSpider",
            "-o",
            "waterscraper_results.json",  # todo -- update this
        ]
    )
except SystemExit:
    pass

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "stepstone"
    start_urls = [
        'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&qs=%5B%7B%22id%22%3A%22216805%22%2C'
        '%22description%22%3A%22Software-Entwickler%2Fin%22%2C%22type%22%3A%22jd%22%7D%5D&companyID=0&cityID=0'
        '&sourceOfTheSearchField=resultlistpage%3Ageneral&searchOrigin=Resultlist_top-search&ke=Software-Entwickler'
        '%2Fin&ws=&ra=30',
        'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&qs=%5B%7B%22id%22%3A%22217249%22%2C'
        '%22description%22%3A%22Software-Architekt%2Fin%22%2C%22type%22%3A%22jd%22%7D%5D&companyID=0&cityID=0'
        '&sourceOfTheSearchField=resultlistpage%3Ageneral&searchOrigin=Resultlist_top-search&ke=Software-Architekt'
        '%2Fin&ws=&ra=30',
        'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&qs=%5B%7B%22id%22%3A%22188428%22%2C'
        '%22description%22%3A%22Wirtschaftsinformatiker%2Fin%22%2C%22type%22%3A%22jd%22%7D%5D&companyID=0&cityID=0'
        '&sourceOfTheSearchField=resultlistpage%3Ageneral&searchOrigin=Resultlist_top-search&ke'
        '=Wirtschaftsinformatiker%2Fin&ws=&ra=30',
        'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&qs=%5B%5D&companyID=0&cityID=0'
        '&sourceOfTheSearchField=offerviewpage%3Ageneral&searchOrigin=Listing-Page-responsive_top-search&ke'
        '=Informatiker&ws=&ra=30 '
    ]

    def parse(self, response):
        next_page = None
        for job in response.css('div.sc-fzXfOw.cvFCUL'):
            yield {
                'link': job.css('a::attr(href)').get()
            }
        results = response.css('div.BottomNavigationContainer-sc-1rtv0xy-3 a.PaginationArrowLink-imp866-0')
        for node in results:
            if node.css('a::attr(data-at)').get() == "pagination-next":
                next_page = node.css('a::attr(href)').get()
                break

        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
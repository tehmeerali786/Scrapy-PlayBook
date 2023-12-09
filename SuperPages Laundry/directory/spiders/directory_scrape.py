import scrapy

class DirectorySpider(scrapy.Spider):
    name='directory'
    allowed_domains=['superpages.com']
    start_urls=['https://www.superpages.com/search?search_terms=Laundromat&geo_location_terms=TX&page=50']
    
    def parse(self, response):
        
        lms = response.css('div.srp-listing')
        
        for lm in lms:
            try:
                lm.css('div.info .info-section.info-secondary .con-group a.weblink-button').attrib['href']
                
                yield {
                    
                    'busines-name' : lm.css('div.info .info-section h2.n span::text').get(),
                    'street-address' : lm.css('div.info .info-section .street-address::text').get(),
                    'description-excerpt' : lm.css('div.info .snippet .body span::text').get(),
                    'phone' : lm.css('div.info .info-section.info-secondary .con-group a span.call-number::text').get(),
                    'website' : lm.css('div.info .info-section.info-secondary .con-group a.weblink-button').attrib['href'],
                }
            except KeyError:
                NoWebsite = 'does not have Website'
                yield {
                    
                    'busines-name' : lm.css('div.info .info-section h2.n span::text').get(),
                    'street-address' : lm.css('div.info .info-section .street-address::text').get(),
                    'description-excerpt' : lm.css('div.info .snippet .body span::text').get(),
                    'phone' : lm.css('div.info .info-section.info-secondary .con-group a span.call-number::text').get(),
                    'website' : NoWebsite,
                }
                
                
            
        next_page = response.css('div.pagination ul li a.next::attr(href)').get()
         
        if next_page is not None:
            
            next_page_url = 'https://www.superpages.com' + next_page
            
            yield response.follow(next_page_url, callback=self.parse)
    
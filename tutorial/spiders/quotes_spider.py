import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://allrecipes.com/recipe/87173/black-bean-lasagna/?internalSource=streams&referringId=87&referringContentType=recipe%20hub&clickId=st_trending_s'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        time_str = response.css('span.ready-in-time::text').extract_first()
        if time_str:
            time_split = time_str.split(' ')
            time = int(time_split[0]) * 60 + int(time_split[2]) if len(time_split) == 4 else int(time_split[0])
        reviews_str = response.css('span.review-count::text').extract_first()
        if reviews_str is not None:
            reviews = reviews_str.split(' ')[0]
        dirty_tags = response.css('span.toggle-similar__title::text').extract()
        clean_tags = []
        for i in dirty_tags:
            i = i.split('\r\n')
            if len(i) == 3:
                clean_tags.append(i[1].strip())
        yield {
            'title': response.xpath('//meta[@property="og:title"]/@content').extract_first(),
            'ingredients': response.css('span.recipe-ingred_txt::text').extract(),
            'instructions': response.css('span.recipe-directions__list--item::text').extract(),
            'avg_reviews': float(response.xpath('//meta[@itemprop="ratingValue"]/@content').extract_first()),
            'num_reviews': int(reviews),
            'time_str': time_str,
            'time': time,
            'tags': clean_tags
        }
        next_page = response.css('div.slider-card__recipes a::attr(href)').extract()
        for i in next_page:
            i = response.urljoin(i)
            yield scrapy.Request(i, callback=self.parse)

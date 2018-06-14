# coding=utf-8

from sandcrawler.scraper import ScraperBase, SimpleScraperBase

class SeriesytvTv(SimpleScraperBase):
    BASE_URL = 'http://www.seriesytv.tv'
    OTHER_URLS = []
    SCRAPER_TYPES = [ ScraperBase.SCRAPER_TYPE_OSP, ]
    LANGUAGE = 'esp'
    MEDIA_TYPES = [ ScraperBase.MEDIA_TYPE_FILM, ScraperBase.MEDIA_TYPE_TV, ]

    URL_TYPES = [ScraperBase.URL_TYPE_SEARCH, ScraperBase.URL_TYPE_LISTING, ]

    def _fetch_search_url(self, search_term, media_type):
        return '{base_url}/buscar/{search_term}'.format(base_url=self.BASE_URL, search_term=search_term)

    def _fetch_no_results_text(self):
        return None

    def _fetch_next_button(self, soup):
        next_button = soup.find('a', text=u'Siguiente')
        if next_button:
            return self.BASE_URL+next_button.href
        return None

    def _parse_search_result_page(self, soup):
        found = 0
        for result in soup.select('div.item'):
            link = result.select_one('a')
            ep_soup = self.get_soup(link.href)
            for ep_link in ep_soup.select('ul#listado a'):
                self.submit_search_result(
                    link_url=ep_link.href,
                    link_title=ep_link.text,
                    image=self.util.find_image_src_or_none(result, 'img'),
                )
                found=1
        if not found:
            return self.submit_search_no_results()
    def _parse_parse_page(self, soup):
        index_page_title = self.util.get_page_title(soup)
        title = soup.find('meta', attrs={'property':'og:title'})['content']
        season, episode = self.util.extract_season_episode(title)
        for link in soup.select('div.tab_content a'):
            self.submit_parse_result(
                index_page_title=index_page_title,
                link_url=link.href,
                link_title=link.text,
                series_season=season,
                series_episode=episode,
            )

# coding=utf-8

from sandcrawler.scraper import ScraperBase, SimpleScraperBase

class FilmeTraduseRo(SimpleScraperBase):
    BASE_URL = 'http://filmetraduse.online'
    OTHER_URLS = []
    SCRAPER_TYPES = [ ScraperBase.SCRAPER_TYPE_OSP, ]
    LANGUAGE = 'ron'
    MEDIA_TYPES = [ ScraperBase.MEDIA_TYPE_FILM, ScraperBase.MEDIA_TYPE_TV, ]

    URL_TYPES = [ScraperBase.URL_TYPE_SEARCH, ScraperBase.URL_TYPE_LISTING, ]

    def _fetch_search_url(self, search_term, media_type):
        return '{base_url}/?&s={search_term}'.format(base_url=self.BASE_URL, search_term=search_term)

    def _fetch_no_results_text(self):
        return u'Niciun rezultat pentru căutarea dvs'

    def _fetch_next_button(self, soup):
        next_button = soup.find('i', 'td-icon-menu-right').find_previous('a')
        if next_button:
            return next_button.href
        return None

    def _parse_search_result_page(self, soup):
        for result in soup.select('div.td-module-thumb'):
            link = result.select_one('a')
            self.submit_search_result(
                link_url=link.href,
                link_title=link.text,
                image=self.util.find_image_src_or_none(result, 'img'),
            )
    def _parse_parse_page(self, soup):
        index_page_title = self.util.get_page_title(soup)
        series_season = series_episode = None
        title = soup.select_one('h1')
        if title and title.text:
            series_season, series_episode = self.util.extract_season_episode(title.text)
        for link in soup.select('div.td-post-content iframe'):
            link_url = link['src']
            if 'http' not in link_url:
                link_url = 'http:'+link_url
            link_title = link.text
            self.submit_parse_result(
                index_page_title=index_page_title,
                link_url=link_url,
                link_title=link_title,
                series_season=series_season,
                series_episode=series_episode,
            )

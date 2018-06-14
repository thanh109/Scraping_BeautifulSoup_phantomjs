# coding=utf-8

from sandcrawler.scraper import ScraperBase, SimpleScraperBase

class SerieStreamingTv(SimpleScraperBase):
    BASE_URL = 'http://www.seriestreaming.online'
    OTHER_URLS = ['http://www.serie-streaming-tv.xyz','http://www.streamingserie.info', 'http://www.streamingserie.biz','http://www.serie-streaming-tv.info', 'http://www.streamingserie.info', 'http://www.serie-streaming.tv', 'http://www.streamingseries.xyz', ]
    SCRAPER_TYPES = [ ScraperBase.SCRAPER_TYPE_OSP, ]
    LANGUAGE = 'fra'
    MEDIA_TYPES = [ ScraperBase.MEDIA_TYPE_FILM, ScraperBase.MEDIA_TYPE_TV, ]

    URL_TYPES = [ScraperBase.URL_TYPE_SEARCH, ScraperBase.URL_TYPE_LISTING, ]

    def setup(self):
        raise NotImplementedError('Deprecated. Duplicate of StreamingSeriesXyz')

    def _fetch_search_url(self, search_term, media_type):
        return '{base_url}/?s={search_term}'.format(base_url=self.BASE_URL, search_term=search_term)

    def _fetch_no_results_text(self):
        return u'Vous pouvez effectuer une nouvelle recherche ou utiliser les archives'

    def _fetch_next_button(self, soup):
        next_button = soup.select_one('a.nextpostslink')
        if next_button:
            return next_button.href
        return None

    def _parse_search_result_page(self, soup):
        for result in soup.select('div.moviefilm'):
            ser_link = result.select_one('a')
            ep_soup = self.get_soup(ser_link.href)
            for ep_link in ep_soup.select('div.keremiya_part a'):
                self.submit_search_result(
                    link_url=ep_link.href,
                    link_title=ep_link.text,
                    image=self.util.find_image_src_or_none(result, 'img'),
                )

    def _parse_parse_page(self, soup):
        index_page_title = self.util.get_page_title(soup)
        series_season = series_episode = None
        title = soup.select_one('h1')
        if title and title.text:
            series_season, series_episode = self.util.extract_season_episode(title.text)
        for link in soup.select('div.filmicerik iframe'):
            self.submit_parse_result(
                index_page_title=index_page_title,
                link_url=link['src'],
                link_title=link.text,
                series_season=series_season,
                series_episode=series_episode,
            )

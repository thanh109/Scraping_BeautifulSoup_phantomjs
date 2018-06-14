# coding=utf-8

from sandcrawler.scraper import ScraperBase, SimpleScraperBase
import re
class UltrafilmizleCom(SimpleScraperBase):
    BASE_URL = 'http://www.ultrafilmizle.co'
    OTHER_URLS = ['http://www.ultrafilmizle.com']
    SCRAPER_TYPES = [ ScraperBase.SCRAPER_TYPE_OSP, ]
    LANGUAGE = 'tur'
    MEDIA_TYPES = [ ScraperBase.MEDIA_TYPE_FILM, ScraperBase.MEDIA_TYPE_TV, ]

    URL_TYPES = [ScraperBase.URL_TYPE_SEARCH, ScraperBase.URL_TYPE_LISTING, ]
    TRELLO_ID = '48bETzmm'

    def _fetch_search_url(self, search_term, media_type):
        return '{base_url}/?s={search_term}'.format(base_url=self.BASE_URL, search_term=search_term)

    def _fetch_no_results_text(self):
        return u'Üzgünüz, kriterlerinize uygun film yok'

    def _fetch_next_button(self, soup):
        next_button = soup.select_one('a.nextpostslink')
        if next_button:
            return next_button.href
        return None

    def _parse_search_result_page(self, soup):
        for result in soup.select('div.ultra-movie'):
            link = result.select_one('a')
            self.submit_search_result(
                link_url=link.href,
                link_title=link.text.strip(),
                image=self.util.find_image_src_or_none(result, 'img'),
            )
    def _parse_parse_page(self, soup):
        index_page_title = self.util.get_page_title(soup)
        series_season = series_episode = None
        title = soup.select_one('h1')
        if title and title.text:
            series_season, series_episode = self.util.extract_season_episode(title.text)
        for movie_link in soup.select('div.keremiya_part a'):
            if 'http' in movie_link['href']:
                video_soup = self.get_soup(movie_link['href'])
                for movie_link in video_soup.select('iframe[allowfullscreen]'):
                    link = movie_link['src']
                    if 'youtube' in link:
                        continue
                    if 'http' not in link:
                        link = 'http:'+link

                    self.submit_parse_result(
                                index_page_title=index_page_title,
                                link_url=link,
                                link_text=movie_link.text,
                                series_season=series_season,
                                series_episode=series_episode,
                    )


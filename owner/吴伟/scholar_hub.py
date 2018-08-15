# <codecell>

!pip install retrying beautifulsoup4 cchardet crossrefapi 

# <codecell>

# -*- coding: utf-8 -*-
"""
Sci-API Unofficial API
- [Search|Download] research papers from [scholar.google.com|sci-hub.io].
- find metadata of an article.
@author Wei Wu
"""

import argparse
import hashlib
import logging
import os
import random
import requests
from bs4 import BeautifulSoup
from retrying import retry
from crossref.restful import Works
import re
from difflib import SequenceMatcher
from urllib.parse import quote_plus
from gensim import utils
import string

# <markdowncell>

# ### http request configuration 

# <codecell>

config = {'USER_AGENT':
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
          
'BLACK_DOMAIN':
  ['www.google.gf',
  'www.google.io',
  'www.google.com.lc',
  'scholar.google.cn'],
          
'PROXIES':{
  'http':
        'http://172.16.103.114:8118',
  'https':
        'http://172.16.103.114:8118'},

'DOMAIN':
  'www.google.com',
'URL_GOOGLE_NEWS':
  "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=2&num=20&start={start}&source=lnms&tbm=nws",
'URL_GOOGLE_SCHOLAR':
  "https://{domain}/scholar?&q={query}&hl={language}&as_sdt=0,5",
'URL_GOOGLE_SCHOLAR_NEXT':
  "https://{domain}/scholar?start={start}&q={query}&hl=zh-CN&as_sdt=0,5",
'URL_GOOGLE_SEARCH':
  "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1&num=20&start={start}",
'COOKIES':
  {'cookies_are':
    "APISID=NeZFvwIlSf_VFLLJ/AOXrafdbi6JV4sc64; SAPISID=5qcC8Xkb7UO3GcNM/AIrZPXgugYcCDpquH; SID=uwV2PDOC2LmzKo50QvpQ19IU0QLQfVaJGDyRRa9--0zos_5rj0RdrxHiphOvMjAlJ_fT2A.; GSP=IN=7e6cc990821af63:LD=zh-CN:CF=4:LM=1526451723:S=L63dTv7IZUmsfik0; 1P_JAR=2018-5-16-8; SIDCC=AEfoLeaD3P2TSefx6nJwwtNUJqHsJ4-tQfiEzmuKwrxHZcO6GJQXGYUFlyjxb2iE2u-xwNIRbzm2siRvgBC2"
         }}

# <codecell>

USER_AGENT = config['USER_AGENT']
DOMAIN = config['DOMAIN']
BLACK_DOMAIN = config['BLACK_DOMAIN']
URL_SEARCH = config['URL_GOOGLE_SEARCH']
PROXIES = config['PROXIES']
URL_SEARCH = config['URL_GOOGLE_SCHOLAR']
URL_NEXT = config['URL_GOOGLE_SCHOLAR_NEXT']

# <codecell>

# log config
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logger = logging.getLogger('Sci-Hub')
logger.setLevel(logging.DEBUG)

# constants
SCIHUB_BASE_URL = 'http://sci-hub.cc/'
SCHOLARS_BASE_URL = 'https://scholar.google.com/scholar'
HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'
}
AVAILABLE_SCIHUB_BASE_URL = [
    'sci-hub.tw', 'sci-hub.hk', 'sci-hub.la', 'sci-hub.mn', 'sci-hub.name',
    'sci-hub.is', 'sci-hub.tv'
    'sci-hub.ws'
    'www.sci-hub.cn'
    'sci-hub.sci-hub.hk', 'sci-hub.sci-hub.tw', 'sci-hub.sci-hub.mn',
    'sci-hub.sci-hub.tv', 'tree.sci-hub.la'
]

# <markdowncell>

# ### string pre-process

# <codecell>

punctuation = u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…'''
RE_PUNCT = re.compile(r'([%s])+' % re.escape(punctuation + string.punctuation),
                      re.UNICODE)
def strip_punctuation(s):
    """Replace punctuation characters with spaces in `s` using :const:`RE_PUNCT`.

    Parameters
    ----------
    s : str

    Returns
    -------
    str
        Unicode string without punctuation characters.

    Examples
    --------
    >>> from wiki_preprocess import strip_punctuation
    >>> strip_punctuation("通常用于计算一个国家、地区、城市全球人口分布状况。")
    u'它通常用于计算一个国家 地区 城市或全球的人口分布状况 '
    >>> strip_punctuation("A semicolon is a stronger break than a comma, but not as much as a full stop!")
    u'A semicolon is a stronger break than a comma  but not as much as a full stop '
    """
    s = utils.to_unicode(s)
    return RE_PUNCT.sub(" ", s)


# <codecell>

class SciHub(object):
    """
    SciHub class can search for papers on Google Scholars
    and fetch/download papers from sci-hub.io
    """

    def __init__(self):
        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning)
        self.sess = requests.Session()
        self.sess.headers = {'user-agent': self.get_random_user_agent()}
        self.available_base_url_list = AVAILABLE_SCIHUB_BASE_URL
        self.base_url = 'http://' + self.available_base_url_list[0] + '/'
        self.works = Works()
        self.sess.proxies = PROXIES
        self.re_bracket = re.compile("\[(.*?)\]\s")

    def get_random_user_agent(self):
        '''choose random user agent as browser header'''
        return random.choice(self.read_file('user_agents.txt', USER_AGENT))

    def get_random_domain(self):
        domain = random.choice(self.read_file('all_domain.txt', DOMAIN))
        if domain in BLACK_DOMAIN:
            self.get_random_domain()
        else:
            return domain

    def read_file(self, filename, default=''):
        # root_folder = os.path.dirname(__file__)
        root_folder = os.getcwd()
        user_agents_file = os.path.join(
            os.path.join(root_folder, 'data'), filename)
        try:
            with open(user_agents_file) as fp:
                data = [_.strip() for _ in fp.readlines()]
        except:
            data = [default]
        return data

    def set_proxy(self, proxy):
        '''
        set proxy for session
        :param proxy_dict:
        :return:
        '''
        # if proxy:
        #     self.sess.proxies = {
        #         "http": proxy,
        #         "https": proxy,
        #     }
        self.sess.proxies = PROXIES

    @retry(
        wait_random_min=200, wait_random_max=2000, stop_max_attempt_number=10)
    def find_meta(self, identifier):
        """ find metadata with title or DOI
        Keyword Arguments:
        identifier --
        """
        try:
            # use identifier article link to find doi from sci-hub.tw
            url = self.base_url + identifier['article_link']
            self.sess.headers = {'user-agent': self.get_random_user_agent()}
            res = self.sess.get(url, verify=False, allow_redirects=False)
            re_bracket = re.compile("\[(.*?)\]\s")
            title = re.sub(re_bracket, "", identifier['name'])
            logger.debug('*' * 80)
            logger.debug("title: %s" % title)
            logger.debug(res.status_code)
            # self.out.ix[title]['status_code'] = res.status_code
            logger.debug("headers: %s" % res.headers['Content-Type'])
            logger.debug('location: %s' % res.headers.get("Location"))
            # self.out.ix[title]['location'] = res.headers.get("Location")
            search_title = True
            # parse response content
            if not res.headers.get("Location"):
                content = res.content
                # fetch DOI
                if len(content) > 2:
                    import cchardet
                    charset = cchardet.detect(content)
                    text = content.decode(charset['encoding'])
                    soup = BeautifulSoup(text, "lxml")
                    script = soup.script.get_text()
                    doi_regexp = '10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+'
                    try:
                        doi_match = re.compile(doi_regexp).findall(script)[0]
                        logger.info("DOI: %s" % doi_match)
                        search_title = False
                        # use crossref API to get metadata
                        works = Works()
                        w1 = works.query(doi_match).sort('relevance').order(
                            'desc')
                        i = 0
                        for item in w1:
                            # TODO: verify title
                            # self.out.ix[title]['DOI'] = item['DOI']
                            return item
                            # return {'meta': item['DOI'], 'url': url}
                    except IndexError:
                        logger.debug('failed to find regexp')
            # search DOI directly with article title from crossref.
            elif search_title:
                works = Works()
                w1 = works.query(title).sort('relevance').order('desc')
                i = 0
                for item in w1:
                    i = i + 1
                    try:
                        # logger.debug('crossref item title ')
                        t = item.get('title')[0]
                        # logger.debug(t)
                        sub_title = item.get('subtitle')[0]
                        # logger.debug(sub_title)
                        # logger.debug("ratio: %s" %
                        #            (SequenceMatcher(a=title, b=t).ratio()))
                    except TypeError:
                        sub_title = ''
                    if SequenceMatcher(
                            a=title, b=t).ratio() > 0.9 or SequenceMatcher(
                                a=title, b=sub_title).ratio(
                                ) > 0.9 or t.startswith(title):
                        logger.debug("DOI %s" % item['DOI'])
                        # self.out.ix[title]['DOI'] = item['DOI']
                        return item
                        # return {'meta': item['DOI'], 'url': url}
                    if i > 18:
                        # logger.debug('[x]%s' % title)
                        # logger.debug(item['title'])
                        return None

        except requests.exceptions.ConnectionError:
            logger.info('{} cannot acess,changing'.format(
                self.available_base_url_list[0]))
            self._change_base_url()

        except requests.exceptions.RequestException as e:

            return {
                'err':
                'Failed to fetch pdf with identifier %s (resolved url %s) due to request exception.'
                % (identifier, url)
            }

    def _change_base_url(self):
        del self.available_base_url_list[0]
        self.base_url = 'http://' + self.available_base_url_list[0] + '/'
        logger.info(
            "I'm changing to {}".format(self.available_base_url_list[0]))

    def req_url(self, query, language=None, start=0, pause=2):
        #        domain = ''
        domain = self.get_random_domain()
        if start > 0:
            url = URL_NEXT
            url = url.format(
                domain=domain, query=quote_plus(query), start=start)
        else:

            url = URL_SEARCH
            url = url.format(
                domain=domain, query=quote_plus(query), language=language)
        return url

    def search(self, query, limit=10, download=False):
        """
        Performs a query on scholar.google.com, and returns a dictionary
        of results in the form {'papers': ...}. Unfortunately, as of now,
        captchas can potentially prevent searches after a certain limit.
        """
        start = 0
        results = {'papers': []}

        while True:
            try:
                self.sess.headers = {'user-agent': self.get_random_user_agent()}
                res = self.sess.get(
                    SCHOLARS_BASE_URL,
                    allow_redirects=True,
                    proxies = PROXIES,
                    params={
                        'q': query,
                        'hl': 'en',
                        'start': start,
                        'as_sdt': '0,5'
                    })
                logger.debug(res.url)
            except requests.exceptions.RequestException as e:
                results[
                    'err'] = 'Failed to complete search with query %s (connection error)' % query
                return results

            s = self._get_soup(res.content)
            papers = s.find_all('div', class_="gs_r")

            if not papers:
                if 'CaptchaRedirect' in res.content:
                    results[
                        'err'] = 'Failed to complete search with query %s (captcha)' % query
                return results

            for paper in papers:
                if not paper.find('table'):
                    source = None
                    pdf = paper.find('div', class_='gs_ggs gs_fl')
                    link = paper.find('h3', class_='gs_rt')
                    # find link type,
                    try:
                        url_type = paper.find(
                            'span', class_='gs_ctg2').get_text()[1:-1]
                    except:
                        url_type = None

                    if pdf:
                        source = pdf.find('a')['href']
                    elif link.find('a'):
                        source = link.find('a')['href']
                    else:
                        continue
                    article_link = link.find('a')['href']
                    title = link.text.replace("\xa0…", "")
                    title = re.sub(self.re_bracket, "", title)
                    title = strip_punctuation(title)
                    results['papers'].append({
                        'name': title,
                        'url': source,
                        'article_link': article_link,
                        'type': url_type
                    })

                    if len(results['papers']) >= limit:
                        return results

            start += 10

    @retry(
        wait_random_min=100, wait_random_max=1000, stop_max_attempt_number=10)
    def download(self, identifier, destination='', path=None):
        """
        Downloads a paper from sci-hub given an indentifier (DOI, PMID, URL).
        Currently, this can potentially be blocked by a captcha if a certain
        limit has been reached.
        """
        data = self.fetch(identifier)

        if not 'err' in data:
            self._save(data['pdf'],
                       os.path.join(destination, path if path else
                                    data['name'].encode('ascii', 'ignore').decode('ascii')))

        return data

    def fetch(self, identifier):
        """
        Fetches the paper by first retrieving the direct link to the pdf.
        If the indentifier is a DOI, PMID, or URL pay-wall, then use Sci-Hub
        to access and download paper. Otherwise, just download paper directly.
        """
        if identifier['type'] == 'PDF':
            url = identifier['url']
        else:
            url = self._get_direct_url(identifier['url'])

        try:
            # verify=False is dangerous but sci-hub.io
            # requires intermediate certificates to verify
            # and requests doesn't know how to download them.
            # as a hacky fix, you can add them to your store
            # and verifying would work. will fix this later.
            self.sess.headers = {'user-agent': self.get_random_user_agent()}
            res = self.sess.get(url, verify=False)

            if res.headers['Content-Type'] != 'application/pdf':
                self._change_base_url()
                raise CaptchaNeedException(
                    'Failed to fetch pdf with identifier %s '
                    '(resolved url %s) due to captcha' % (identifier, url))
                # return {
                #     'err': 'Failed to fetch pdf with identifier %s (resolved url %s) due to captcha'
                #            % (identifier, url)
                # }
            else:
                return {
                    'pdf': res.content,
                    'url': url,
                    'name': identifier['name'] + '.pdf'
                    #                    'name': self._generate_name(res)
                }

        except requests.exceptions.ConnectionError:
            logger.info('{} cannot acess,changing'.format(
                self.available_base_url_list[0]))
            self._change_base_url()

        except requests.exceptions.RequestException as e:

            return {
                'err':
                'Failed to fetch pdf with identifier %s (resolved url %s) due to request exception.'
                % (identifier, url)
            }

    def _get_direct_url(self, identifier):
        """
        Finds the direct source url for a given identifier.
        """
        id_type = self._classify(identifier)

        return identifier if id_type == 'url-direct' \
            else self._search_direct_url(identifier)

    def _search_direct_url(self, identifier):
        """
        Sci-Hub embeds papers in an iframe. This function finds the actual
        source url which looks something like https://moscow.sci-hub.io/.../....pdf.
        """
        self.sess.headers = {'user-agent': self.get_random_user_agent()}
        res = self.sess.get(self.base_url + identifier, verify=False)
        s = self._get_soup(res.content)
        iframe = s.find('iframe')
        if iframe:
            return iframe.get('src') if not iframe.get('src').startswith('//') \
                else 'http:' + iframe.get('src')

    def _classify(self, identifier):
        """
        Classify the type of identifier:
        url-direct - openly accessible paper
        url-non-direct - pay-walled paper
        pmid - PubMed ID
        doi - digital object identifier
        """
        if (identifier.startswith('http') or identifier.startswith('https')):
            if identifier.endswith('pdf'):
                return 'url-direct'
            else:
                return 'url-non-direct'
        elif identifier.isdigit():
            return 'pmid'
        else:
            return 'doi'

    def _save(self, data, path):
        """
        Save a file give data and a path.
        """
        with open(path, 'wb') as f:
            f.write(data)

    def _get_soup(self, html):
        """
        Return html soup.
        """
        return BeautifulSoup(html, 'html.parser')

    def _generate_name(self, res):
        """
        Generate unique filename for paper. Returns a name by calcuating
        md5 hash of file contents, then appending the last 20 characters
        of the url which typically provides a good paper identifier.
        """
        name = res.url.split('/')[-1]
        pdf_hash = hashlib.md5(res.content).hexdigest()
        return '%s-%s' % (pdf_hash, name[-20:])


class CaptchaNeedException(Exception):
    pass


# <codecell>

def scholar_hub(title ,num_limit):
    sh = SciHub()
    # retrieve 5 articles on Google Scholars related to 'nlp'
    results = sh.search(title, num_limit)
    return results

# <codecell>


import scrapy
import json
from bs4 import BeautifulSoup
from pathlib import Path
import unicodedata


def get_urls(filename, urls):
    """ Build absolute urls name by aadding the prefix "https://www.stepstone.de" to them """
    dir_path = str(Path(__file__).resolve().parents[1])
    print("-----------------------------" + dir_path)
    with open(filename, 'r') as f:
        data = json.load(f)
        l = list(data)
        link_set = set()
        [link_set.add(dict(link)['link']) for link in l]
        print(f'number of links from {len(l)} to {len(link_set)}: number of duplicate {len(l) - len(link_set)}')
        # print(data)
        # data = json.loads(data)
        for link in link_set:
            #d = dict(link)
            #urls.append("https://www.stepstone.de" + d['link'])
            urls.append("https://www.stepstone.de" + link)
    return urls


class QuotesSpider(scrapy.Spider):
    """
    This class parse a given stepstone job description to extract the job description as well as the job profile
    """

    name = "jobparser"
    """ Name of the parser used by scrapy in the console"""
    urls = []

    start_urls = get_urls('stepstone_links_20210416.json', urls)
    #start_urls = ['https://www.stepstone.de/stellenangebote--Informatiker-m-w-d-IT-Koordination-Stassfurt-TechniSat-Teledigital-GmbH--7128799-inline.html?suid=c0e1269b-3d9b-46a0-be57-73d5b9816ed7&rltr=4_4_25_dynrl_m_0_1_0_0_0']
    """The list of urls provided from the file links_20201012.json"""

    def parse(self, response):
        for job in response.css('div.listing-content'):
            header = job.css('div.js-app-ld-HeaderStepStoneBlock').get()
            job_title = job.css('h1.listing__job-title.at-header-company-jobTitle.sc-cvbbAY.gVaAgS').get()
            intro = job.css('div.sc-elJkPf.ksRbbv').getall()[0]
            task = job.css('div.sc-elJkPf.ksRbbv').getall()[1]
            profile = job.css('div.sc-elJkPf.ksRbbv').getall()[2]
            offer = job.css('div.sc-elJkPf.ksRbbv').getall()[3]
            contact = job.css('div.sc-elJkPf.ftSmMc').get()
            yield {
                'id_block': self.extract_text_blocks(header),
                'job_title': self.extract_text_blocks(job_title),
                'intro_block': self.extract_text_blocks(intro),
                'task_block': self.extract_text_blocks(task),
                'profile_block': self.extract_text_blocks(profile),
                'offer_block': self.extract_text_blocks(offer),
                'contact_block': self.extract_text_blocks(contact),
            }

    def extract_text_blocks(self, css):
        soup = BeautifulSoup(css, "lxml")
        result = ""
        whitelist = [
            'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5'
        ]
        elements = soup.findAll(whitelist)
        for el in elements:
            result += unicodedata.normalize("NFKD",el.getText(strip=True)) + '\n'
        return result


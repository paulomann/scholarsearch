%load_ext autoreload
%autoreload 2
from bs4 import BeautifulSoup
import urllib3
import re
from urllib.request import Request
from urllib.parse import quote, unquote
from typing import Union, List

SCHOLAR_URL = "https://scholar.google.com/scholar?" \
    + "hl=en" \
    + "&q={query}"

title = "Multimodal Model-Agnostic Meta-Learning via Task-Aware Modulation"

def encode_url(url, params_dict):
    for k, v in params_dict.items():
        params_dict[k] = quote(v)
    return url.format(**params_dict)
    

class GoogleScholarParser:
    
    def __init__(self, base_url=SCHOLAR_URL):
        self.base_url = base_url
        self.http = urllib3.PoolManager()
        self.soup = None

    def get_number_of_citations(self, paper_title: str) -> Union[int, None]:
        try:
            search_url = encode_url(self.base_url, {"query": paper_title})
            page = self.http.request('GET', search_url)
            self.soup = BeautifulSoup(page.data, 'html.parser')
            tag = self.soup.find_all(lambda tag: tag.name == "a" and "Cited by" in tag.text)[0]
            cited_regex_string = "Cited by (\d+)"
            regex_match = re.search(cited_regex_string, tag.text)
            if regex_match:
                return int(regex_match.group(1))
        except Exception as e:
            print("ERROR: " + repr(e))
        
gsp = GoogleScholarParser()
gsp.get_number_of_citations(title)

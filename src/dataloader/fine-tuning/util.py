import requests
from enum import Enum
from bs4 import BeautifulSoup
import re

class Request():
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url if base_url else ""
    
    def get(self, url: str, headers=None, verbose=1):
        response = requests.get(url=self.base_url+url, headers=headers)
        if verbose == 1:
            print(f"Request URL - {url} ({response.status_code})")
        return response

class BeautifulSoupUtil():
    
    class Type(Enum):
        HTML = "html.parser"
        HTML5 = "html5lib"
        XML = "lxml"
        
    def _get_object(data, type: "BeautifulSoupUtil.Type", verbose=1) -> BeautifulSoup:
        if verbose == 1:
            print(f"parse -> {type.value}")
        return BeautifulSoup(markup=data, features=type.value)
    
    def parse_html(data, verbose=1) -> BeautifulSoup:
        return BeautifulSoupUtil._get_object(data=data, type=BeautifulSoupUtil.Type.HTML, verbose=verbose)

class Scrape():
    
    def __init__(self: "Scrape", base_url: str = None) -> None:
        self.base_url = base_url if base_url else ""
        
    def get_html(self: "Scrape", resource_path: str, verbose=1) -> BeautifulSoup:
        # Fetch Data
        request = Request()
        url = self.base_url + resource_path
        response = request.get(url=url, verbose=verbose)
        # get HTML
        return BeautifulSoupUtil.parse_html(data=response.text, verbose=verbose)
    
class Regex():
    
    def remove_html_tags(html):
        clean_text = re.sub(r'<.*?>', '', html)
        return clean_text
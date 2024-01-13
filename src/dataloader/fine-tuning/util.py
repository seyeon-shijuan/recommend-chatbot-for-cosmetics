import requests
from enum import Enum
from bs4 import BeautifulSoup
import re
from datetime import datetime

class DateUtil():
    
    def get_current_time_form() -> str:
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H.%M.%S")
        return formatted_time

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
    
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    html_tag_pattern = re.compile(r"<.*?>")
    escape_pattern = re.compile(r"(\w+)-\n(\w+)")
    escape_unicode_pattern = re.compile(r"\\[tn]|\\u200b")
    escape_unicode2_pattern = re.compile(r"[\n\t\u200b]")
    
    def remove_html_tags(html):
        cleaned_text = re.sub(Regex.html_tag_pattern, "", html)
        return cleaned_text
    
    def remove_escape(text):
        cleaned_text = re.sub(Regex.escape_pattern, r"\1\2", text)
        return cleaned_text
    
    def remove_escape_unicode(text):
        cleaned_text = re.sub(Regex.escape_unicode_pattern, "", text)
        return cleaned_text
    
    def remove_escape_unicode2(text):
        cleaned_text = re.sub(Regex.escape_unicode2_pattern, "", text)
        return cleaned_text
    
    def remove_url(text):
        cleaned_text = re.sub(Regex.url_pattern, "", text)
        return cleaned_text
    
class StringUtil():
    
    def clean(text: str) -> str:
        text = Regex.remove_html_tags(text)
        text = Regex.remove_escape_unicode2(text)
        text = Regex.remove_url(text)
        text = text.strip()
        return text
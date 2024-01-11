from functools import reduce
from urllib.parse import urlencode
from enum import Enum
from util import Scrape
from typing import Callable

class Item():
    
    def __init__(self, item):
        self.title = item["title"]
        self.link = item["link"]
        self.description = item["description"]
        
    def load_qna(self, loader: Scrape, function: Callable[[Scrape, int], tuple[str, list[str]]]):
        question, answers = function(loader, self.link)
        
    def __str__(self):
        return f"""
    title: {self.title}
    link: {self.link}
    description: {self.description}
    """

class Naver지식IN():
    
    def __init__(self, json: dict):
        self.lastBuildDate = json["lastBuildDate"]
        self.total = json["total"]
        self.start = json["start"]
        self.display = json["display"]
        self.items = [ Item(item) for item in json["items"] ]
        
    def __len__(self):
        return len(self.items)
    
    def __str__(self):
        return f"""
    < Naver 지식IN >
    lastBuildDate: {self.lastBuildDate}
    total: {self.total}
    start: {self.start}
    display: {self.display}
    items: 
    {reduce(lambda a, b: a + str(b), self.items, "")}
    """
    
class NaverSort(Enum):
    SIMILARITY = "sim"
    DATE = "date"
    RATING = "point"

class NaverQueryParameter():
    
    def __init__(self, query: str, display: int = 100, start: int = 1, sort: NaverSort = NaverSort.SIMILARITY):
        self.query = query
        self.display = display
        self.start = start
        self.sort = sort.value
        
    def __str__(self):
        return urlencode(self.__dict__)
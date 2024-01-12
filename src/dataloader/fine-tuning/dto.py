from functools import reduce
from urllib.parse import urlencode
from enum import Enum
from util import Scrape, Regex
from typing import Callable, Union

class Item():
    
    def __init__(self, item):
        self.title = item["title"]
        self.link = item["link"]
        self.description = item["description"]
        
    def load_qna(self, loader: Scrape, function: Callable[[Scrape, str], tuple[str, list[str]]]) -> Union[tuple[str, str], tuple[str, list[str]]]:
        question, answer = function(loader, self.link)
        return question, answer
        
    def __str__(self):
        return f"""
    < Item >
    title: {self.title}
    link: {self.link}
    description: {self.description}
    """

class FetchType(Enum):
    SINGLE = "S"
    PAIR = "P"

class Naver지식IN():
    
    def __init__(self, json: dict):
        
        try:
            self.lastBuildDate = json["lastBuildDate"]
            self.total = json["total"]
            self.start = json["start"]
            self.display = json["display"]
            self.items = [ Item(item) for item in json["items"] ]
            self.loader = Scrape()
        except:
            print(f"response:\n{json}")
        
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
    
    def load_single_answer(loader: Scrape, link: str) -> tuple[str, str]:
        
        soup = loader.get_html(resource_path=link, verbose=0)
        question , answer = None, None
        
        question = soup.select_one("div.c-heading__content")
        if question is not None:
            question = Regex.remove_html_tags(question.text)
            question = Regex.remove_escape_unicode2(question)
            question = Regex.remove_url(question)
        
            adopt_check = soup.select_one("div.checkText")
            if adopt_check is not None:
                parent_answer = adopt_check.find_parent(name="div", attrs={"class": "answer-content__item"})
                answer = parent_answer.select_one("div.se-main-container")
                
                if answer is not None:
                    answer = Regex.remove_html_tags(answer.text)
                    answer = Regex.remove_escape_unicode2(answer)
                    answer = Regex.remove_url(answer)

        return question, answer

    def load_multiple_answer(loader: Scrape, link: str) -> tuple[str, str]:
        soup = loader.get_html(resource_path=link)
        q = soup.select_one("div.c-heading__content")
        adopt_check = soup.select_one("div.checkText")
        if adopt_check is not None:
            # 채택 답변
            adopt_check.find_parent(name="div", attrs={"class": "answer-content__item"})
            pass
        
    
    def fetch_item(self, fetch_type: FetchType, range: slice = slice(None)) -> list[tuple[str, str] | tuple[str, list[str]]]:
        
        load_function = None
        if fetch_type == FetchType.SINGLE:
            load_function = Naver지식IN.load_single_answer
        elif fetch_type == FetchType.PAIR:
            load_function = Naver지식IN.load_multiple_answer
        else:
            raise ValueError("SINGLE or PAIR only.")
        
        list = [   
            item.load_qna(loader=self.loader, function=load_function) 
            for item in self.items[range] 
        ]
        
        filter_qna = lambda qna: qna[0] is not None and qna[1] is not None
        filtered_list = filter(filter_qna, list)
        return filtered_list
    
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
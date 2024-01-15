from functools import reduce
from urllib.parse import urlencode
from enum import Enum
from util import Scrape, Regex, StringUtil
from typing import Callable, Union

class Item():
    
    def __init__(self, item):
        self.title = item["title"]
        self.link = item["link"]
        self.description = item["description"]
        
    def load_qna(self, loader: Scrape, function: Callable[[Scrape, str], Union[tuple[str, str], tuple[str, str, str]]]) -> Union[tuple[str, str], tuple[str, str, str]]:
        return function(loader, self.link)
        
    def __str__(self):
        return f"""
    < Item >
    title: {self.title}
    link: {self.link}
    description: {self.description}
    """

class FetchType(Enum):
    SINGLE = "single"
    PAIR = "pair"

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
            question = StringUtil.clean(question.text)
        
            adopt_check = soup.select_one("div.checkText")
            if adopt_check is not None:
                parent_answer = adopt_check.find_parent(name="div", attrs={"class": "answer-content__item"})
                answer = parent_answer.select_one("div.se-main-container")
                
                if answer is not None:
                    answer = StringUtil.clean(answer.text)

        return question, answer

    def load_pair_answer(loader: Scrape, link: str) -> tuple[str, tuple[str, str]]:
        
        soup = loader.get_html(resource_path=link, verbose=0)
        question , adopt_answer, other_answer = None, None, None
        
        question = soup.select_one("div.c-heading__content")
        if question is not None:
            question = StringUtil.clean(question.text)
        
            adopt_check = soup.select_one("div.checkText")
            if adopt_check is not None:
                
                
                parent_answer = adopt_check.find_parent(name="div", attrs={"class": "answer-content__item"})
                adopt_answer = parent_answer.select_one("div.se-main-container")
                
                answer_list = soup.select("div.answer-content__item")
                
                filtered_answer_list = []
                for answer in answer_list:
                    profile_card = answer.select_one("div.profile_card")
                    text = profile_card.text.strip()
                    if not text.startswith("사용자 신고"):
                        filtered_answer_list.append(answer)
                    
                if adopt_answer is not None:
                    adopt_answer = StringUtil.clean(adopt_answer.text)
                
                if len(filtered_answer_list) > 2:
                    other_answer = filtered_answer_list[-1].select_one("div.se-main-container")
                    if other_answer is not None:
                        other_answer = StringUtil.clean(other_answer.text)

        return question, adopt_answer, other_answer
        
    
    def fetch_item(self, fetch_type: FetchType, range: slice = slice(None)) -> list[tuple[str, str] | tuple[str, tuple[str]]]:
        
        load_function = None
        if fetch_type == FetchType.SINGLE:
            load_function = Naver지식IN.load_single_answer
        elif fetch_type == FetchType.PAIR:
            load_function = Naver지식IN.load_pair_answer
        else:
            raise ValueError("SINGLE or PAIR only.")
        
        qna_list = [
            item.load_qna(loader=self.loader, function=load_function) 
            for item in self.items[range] 
        ]
        
        filter_qna = lambda qna: all(val is not None for val in qna)
        filtered_list = filter(filter_qna, qna_list)
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
from collection import Collection
from dto import FetchType
import configparser
import pandas as pd
from util import FileUtil

config = configparser.ConfigParser()
config.read(filenames="src/dataloader/data_config.env")

naver = config["naver"]
search_keywords = [ keyword.strip() for keyword in naver["Search-Keywords"].split(",") ] 
instruction = naver["Instruction"]

def save_file(data: pd.DataFrame, filename: str):
    
    FileUtil.save_jsonl(data=data, path=filename)
    FileUtil.save_csv(data=data, path=filename, sep="|")
    data_info = f"""
    Search keywords: {search_keywords}
    Instruction: {instruction}
    Columns: {list(data.columns)}
    """
    FileUtil.save_txt(text=data_info, path=f"{filename}-info")
    
collection = Collection(set_filename="src/dataloader/data_config.env")

data_single_set, filename = collection.collect(fetch_type=FetchType.SINGLE, keywords=search_keywords, instruction=instruction)
save_file(data=data_single_set, filename=filename)

data_pair_set, filename = collection.collect(fetch_type=FetchType.PAIR, keywords=search_keywords, instruction=instruction)
save_file(data=data_pair_set, filename=filename)

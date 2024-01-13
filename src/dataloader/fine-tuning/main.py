from collection import Collection
from dto import FetchType
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read(filenames="src/dataloader/data_config.env")

naver = config["naver"]
search_keywords = [ keyword.strip() for keyword in naver["Search-Keywords"].split(",") ] 
instruction = naver["Instruction"]

def save_file(data: pd.DataFrame, filename: str):
    
    with open(f"{filename}.jsonl", "w", encoding="utf-8") as file:
        for _, row in data.iterrows():
            file.write(row.to_json(force_ascii=False) + '\n')

    data.to_csv(f"{filename}.csv", sep="|", index=False)
    
    with open(f"{filename}-info.txt", "w", encoding="utf-8") as file:
        file.write(f"Search keywords: {search_keywords}" + '\n')
        file.write(f"Instruction: {instruction}" + '\n')
        file.write(f"Columns: {data.columns}" + '\n')

collection = Collection(set_filename="src/dataloader/data_config.env")

data_single_set, filename = collection.collect(fetch_type=FetchType.SINGLE, keywords=search_keywords, instruction=instruction)
save_file(data=data_single_set, filename=filename)

data_pair_set, filename = collection.collect(fetch_type=FetchType.PAIR, keywords=search_keywords, instruction=instruction)
save_file(data=data_pair_set, filename=filename)

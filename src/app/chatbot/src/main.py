from fastapi import FastAPI
from src.api.chat_api import chatbotAPIRouter
from src.api.llm_serivce import Prompt
from uvicorn import run
import configparser

app = FastAPI()

config = configparser.ConfigParser()
config.read("config.env")

server = config["server"]
server_port = int(server["port"])

def start():
    run(app, port=server_port)

@app.get(path="/test")
def test(text: str = "test"):
    return chatbotAPIRouter.test(text)

@app.post(path="/prompt")
async def prompt(prompt: Prompt):
    
    print("POST", type(prompt))
    return chatbotAPIRouter.prompt(prompt)
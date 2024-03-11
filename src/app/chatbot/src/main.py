from fastapi import FastAPI
from src.api.chat_api import chatbotAPIRouter
from src.api.llm_serivce import Prompt, PromptResponse
from uvicorn import run
from uvicorn.config import LOGGING_CONFIG
import configparser
import warnings

warnings.filterwarnings('ignore')

app = FastAPI()

config = configparser.ConfigParser()
config.read("config.env")

server = config["server"]
server_port = int(server["port"])

def start():
    DATE_FMT = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s [%(levelname)s] [%(filename)s] [%(process)d] %(client_addr)s - "%(request_line)s" %(status_code)s'
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(levelname)s] [%(filename)s] - %(message)s"
    LOGGING_CONFIG["formatters"]["default"]["datefmt"] = DATE_FMT
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = DATE_FMT
    run(app, port=server_port)

@app.get(path="/test")
def test(text: str = "test"):
    return chatbotAPIRouter.test(text=text)

@app.post(path="/prompt")
async def prompt(prompt: Prompt) -> PromptResponse:
    return chatbotAPIRouter.prompt(prompt=prompt)
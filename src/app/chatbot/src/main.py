from fastapi import FastAPI
from src.api.inference_api import chatbotAPIRouter
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

@app.get(path="/prompt")
def prompt(prompt):
    return chatbotAPIRouter.prompt(prompt)
from fastapi import FastAPI
from src.api.inference_api import inferenceAPIRouter
from uvicorn import run
import configparser

app = FastAPI()

config = configparser.ConfigParser()
config.read("config.env")

server = config["server"]
server_port = int(server["port"])

def start():
    run(app, port=server_port)

@app.get("/test")
def test():
    return inferenceAPIRouter.inference()


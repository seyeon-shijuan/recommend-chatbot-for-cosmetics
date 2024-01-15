from fastapi import FastAPI
from src.api.recommend_api import recommendationAPIRouter
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
def test(text: str = "test"):
    return recommendationAPIRouter.test(text)

@app.get("/collabo/filters")
def test(product_name: str):
    return recommendationAPIRouter.recommend_product(product_name=product_name)

@app.get("/product")
def test(id: int):
    return recommendationAPIRouter.product_info(product_id=id)
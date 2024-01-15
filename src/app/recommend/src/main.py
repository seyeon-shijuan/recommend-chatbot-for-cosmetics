from fastapi import FastAPI
from src.api.recommend_api import recommendationAPIRouter
from uvicorn import run
import configparser


IF_PYCHARM = True

app = FastAPI()
config = configparser.ConfigParser()

if IF_PYCHARM:
    config.read("../config.env")
else:
    config.read("config.env")

server = config["server"]
server_port = int(server["port"])


def start():
    run(app, port=server_port)


@app.get("/test")
def test(text: str = "test"):
    return recommendationAPIRouter.test(text)


@app.get("/collabo/filters")
async def recommend_product(product_name: str):
    return recommendationAPIRouter.recommend_product(product_name=product_name)


@app.get("/product")
def test(id: int):
    return recommendationAPIRouter.product_info(product_id=id)


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=server_port)
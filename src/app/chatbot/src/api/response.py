from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    category: str
    skin_type: str
    contents: list[str]
    image_url: str
    ingredients: str

@dataclass
class CollaboFilterResponse:
    product_list: list[Product]
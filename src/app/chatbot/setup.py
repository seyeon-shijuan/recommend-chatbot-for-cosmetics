from setuptools import setup

setup(
    name="cosmetic-chat-app",
    version="0.1",
    description='cosmetics chatbot',
    packages=[
        "src", 
        "src/api",
        "src/model"
    ],
    install_requires=[
        "configparser",
        "uvicorn",
        "fastapi",
        "pydantic",
        "transformers",
        "peft",
        "pytorch",
        "langchain",
        "langchain_community"
    ],
    entry_points={
        'console_scripts': [
            'cosmetic-chat = src.main:start',
        ],
    }
)
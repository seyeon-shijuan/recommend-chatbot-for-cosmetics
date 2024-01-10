from setuptools import setup, find_packages

setup(
    name="chatbot-app",
    version="0.1",
    description='llm chatbot',
    packages=find_packages(),
    install_requires=[
        "fastapi"
    ]
)
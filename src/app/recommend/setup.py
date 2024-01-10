from setuptools import setup

setup(
    name="cosmetic-rec-app",
    version="0.1",
    description='cosmetics recommendation system',
    packages=[
        "src", 
        "src/api"
    ],
    install_requires=[
        "configparser",
        "uvicorn",
        "fastapi"
    ],
    entry_points={
        'console_scripts': [
            'cosmetic-rec = src.main:start',
        ],
    }
)
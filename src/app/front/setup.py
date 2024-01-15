from setuptools import setup

setup(
    name="cosmetic-front-app",
    version="0.1",
    description='cosmetics front system',
    packages=[
        "src", 
        "src/api"
    ],
    install_requires=[
        "streamlit"
    ],
    entry_points={
        'console_scripts': [
            'cosmetic-front = src.main:start',
        ],
    }
)
from setuptools import setup

setup(
    name="cosmetic-front-app",
    version="0.1",
    description='cosmetics front system',
    packages=[
        "src", 
        "src/api"
        "src/pages"
    ],
    install_requires=[
        "streamlit",
        "pandas",
        "sqlite3",
        "requests",
        "streamlit_lottie"
    ],
    entry_points={
        'console_scripts': [
            'cosmetic-front = src.main:start',
        ],
    }
)
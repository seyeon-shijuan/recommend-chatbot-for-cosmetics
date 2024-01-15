import subprocess
from src.config import load

def start():
    config = load()
    server_config = config["server"]
    streamlit_command = f"streamlit run src/home.py --server.address {server_config['address']} --server.port {server_config['port']}"
    subprocess.run(streamlit_command, shell=True)

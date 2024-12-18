import os
from dotenv import load_dotenv

def load_environment_variables():
    base_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    load_dotenv(dotenv_path=base_env_path)

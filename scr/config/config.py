# ProjectZoo/config/config.py

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../../protect.env')

TOKEN = os.getenv('TOKEN')

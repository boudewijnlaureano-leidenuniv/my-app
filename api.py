import openai
import os
from dotenv import load_dotenv, dotenv_values
import sys

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
print(API_KEY)
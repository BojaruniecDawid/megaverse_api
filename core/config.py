import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = "https://challenge.crossmint.io/api"
    CANDIDATE_ID = os.getenv("CANDIDATE_ID")
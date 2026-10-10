import os

import psycopg
from dotenv import load_dotenv

load_dotenv()
def connect():
    return psycopg.connect(host=os.getenv('POSTGRES_HOST','localhost'),port=os.getenv('POSTGRES_PORT','5432'),dbname=os.getenv('POSTGRES_DB'),user=os.getenv('POSTGRES_USER'),password=os.getenv('POSTGRES_PASSWORD'))

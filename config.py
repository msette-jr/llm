# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "banco_padrao.db")
CACHE_DB_PATH = os.getenv("CACHE_DB_PATH", "cache_respostas.db")
MODEL_PATH = os.getenv(
    "MODEL_PATH", 
    "~/Library/Application Support/nomic.ai/GPT4All/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf"
)

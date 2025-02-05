import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

"""
dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)
"""
load_dotenv(find_dotenv('.env'))

class Config:
    NEO4J_URI = os.environ.get('NEO4J_URI','')
    NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME', 'neo4j')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD','')
    AURA_INSTANCEID = os.environ.get('AURA_INSTANCEID','')
    AURA_INSTANCENAME = os.environ.get('AURA_INSTANCENAME','')

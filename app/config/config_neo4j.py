import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

#Configuration for Neo4j connection
NEO4J_URI= os.environ["NEO4J_URI"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from neo4j import GraphDatabase
import redis

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Edugraph")

try:
    mongo_client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    mongo_client.admin.command('ping')
    mongo_db = mongo_client[MONGO_DB_NAME]
    print("MongoDB Connected.")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

try:
    
    neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    neo4j_driver.verify_connectivity()
    print("Neo4j Connected.")
except Exception as e:
    print(f"Neo4j connection failed: {e}")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    redis_client.ping()
    print("Connected to Redis (Docker)")
except Exception as e:
    print("Redis connection failed:", e)

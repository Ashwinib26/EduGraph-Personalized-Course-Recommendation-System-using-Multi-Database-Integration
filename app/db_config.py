from pymongo import MongoClient
from neo4j import GraphDatabase
import redis

# MongoDB (local)
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["edugraph"]

# Neo4j (local)
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test123"))

# Redis (Docker)
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

import os
from dotenv import load_dotenv

load_dotenv()

from pymongo import MongoClient
from neo4j import GraphDatabase
import redis
import json
import time

MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASS = os.getenv("MONGO_PASS", "example")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "test123")
NEO4J_BOLT = os.getenv("NEO4J_BOLT", "bolt://localhost:7687")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def mongo_connect():
    uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"
    client = MongoClient(uri)
    db = client['edudb']
    return db

def neo4j_connect():
    driver = GraphDatabase.driver(NEO4J_BOLT, auth=(NEO4J_USER, NEO4J_PASS))
    return driver

def redis_connect():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    return r

def seed_mongo(db):
    students = db.students
    courses = db.courses

    student_doc = {"student_id": 101, "name": "Ashwini", "interests": ["AI", "Data Science"]}
    course_doc = {"course_id": 301, "title": "Deep Learning with Python", "tags": ["AI", "Neural Networks", "Python"], "rating": 4.7}

    students.update_one({"student_id": student_doc["student_id"]}, {"$set": student_doc}, upsert=True)
    courses.update_one({"course_id": course_doc["course_id"]}, {"$set": course_doc}, upsert=True)

    print("MongoDB: seeded student and course.")

def seed_neo4j(driver):
    with driver.session() as session:
        session.run("MERGE (s:Student {student_id: $id, name: $name})",
                    id=101, name="Ashwini")
        session.run("MERGE (c:Course {course_id: $cid, title: $title})",
                    cid=301, title="Deep Learning with Python")
        session.run("""
            MATCH (s:Student {student_id:$id}), (c:Course {course_id:$cid})
            MERGE (s)-[:ENROLLED_IN]->(c)
        """, id=101, cid=301)
    print("Neo4j: seeded Student, Course and ENROLLED_IN relation.")

def cache_in_redis(r):
    key = "user:101:recommendations"
    value = json.dumps([{"course_id": 301, "title": "Deep Learning with Python", "score": 0.95}])
   
    r.set(key, value, ex=3600)
    print("Redis: cached recommendations under", key)

def verify_all(db, driver, r):
   
    stud = db.students.find_one({"student_id": 101})
    print("MongoDB student:", stud)

    with driver.session() as session:
        res = session.run("MATCH (s:Student)-[:ENROLLED_IN]->(c:Course) WHERE s.student_id=$id RETURN s.name AS student, c.title AS course",
                          id=101)
        for record in res:
            print("Neo4j relation:", record["student"], "->", record["course"])

    cached = r.get("user:101:recommendations")
    print("Redis cached recommendations:", cached)

def main():
    print("Connecting to services...")
    db = mongo_connect()
    driver = neo4j_connect()
    r = redis_connect()

    time.sleep(2)

    seed_mongo(db)
    seed_neo4j(driver)
    cache_in_redis(r)
    verify_all(db, driver, r)

    driver.close()

if __name__ == "__main__":
    main()

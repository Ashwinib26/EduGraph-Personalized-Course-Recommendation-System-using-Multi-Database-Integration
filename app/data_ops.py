from app.db_config import mongo_db, neo4j_driver, redis_client

def get_student_from_mongo(student_id):
    student = mongo_db.students.find_one({"student_id": student_id}, {"_id": 0})
    return student

def get_recommendations_from_neo4j(student_id):
    with neo4j_driver.session() as session:
        query = """
        MATCH (s:Student {student_id: $student_id})-[:INTERESTED_IN]->(sk:Skill)<-[:HAS_SKILL]-(c:Course)
        RETURN c.title AS course
        """
        result = session.run(query, student_id=student_id)
        return [record["course"] for record in result]

def cache_recommendations(student_id, recommendations):
    redis_client.set(f"user:{student_id}:recs", str(recommendations), ex=3600)

def get_cached_recommendations(student_id):
    cached = redis_client.get(f"user:{student_id}:recs")
    return eval(cached) if cached else None

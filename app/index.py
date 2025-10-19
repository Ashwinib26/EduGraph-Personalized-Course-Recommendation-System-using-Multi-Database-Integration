from db_config import mongo_db, neo4j_driver, redis_client

def get_all_students():
    students = list(mongo_db["students"].find({}, {"_id": 0}))
    return students

def get_student_graph_data(student_name):
    query = """
    MATCH (s:Student {name: $name})
    OPTIONAL MATCH (s)-[:HAS_SKILL]->(sk:Skill)
    OPTIONAL MATCH (s)-[:ENROLLED_IN]->(c:Course)
    RETURN s.name AS student, collect(DISTINCT sk.name) AS skills, collect(DISTINCT c.title) AS courses
    """
    with neo4j_driver.session() as session:
        result = session.run(query, name=student_name)
        return result.single()


def recommend_courses(student_name):
    cached = redis_client.get(f"recommend:{student_name}")
    if cached:
        print("📦 Using cached recommendations from Redis")
        return eval(cached)

    print("🔍 Fetching new recommendations from Neo4j...")
    query = """
    MATCH (s:Student {name: $name})-[:HAS_SKILL]->(sk:Skill)<-[:REQUIRES_SKILL]-(c:Course)
    WHERE NOT (s)-[:ENROLLED_IN]->(c)
    RETURN DISTINCT c.title AS recommended_courses
    """
    with neo4j_driver.session() as session:
        result = session.run(query, name=student_name)
        courses = [r["recommended_courses"] for r in result]

    redis_client.setex(f"recommend:{student_name}", 300, str(courses))
    return courses

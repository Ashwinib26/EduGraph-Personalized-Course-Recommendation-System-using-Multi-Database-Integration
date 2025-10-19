from app.data_ops import (
    get_student_from_mongo,
    get_recommendations_from_neo4j,
    get_cached_recommendations,
    cache_recommendations
)

def get_recommendations(student_id):
    # Check Redis cache
    # cached = get_cached_recommendations(student_id)
    # if cached:
    #     print("📦 Returning from Redis cache")
    #     return cached

    student = get_student_from_mongo(student_id)
    if not student:
        return ["No student found"]

    recs = get_recommendations_from_neo4j(student_id)

    if recs:
        cache_recommendations(student_id, recs)

    return recs or ["No recommendations found"]

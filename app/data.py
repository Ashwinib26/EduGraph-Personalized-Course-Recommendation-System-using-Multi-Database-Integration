from db_config import mongo_db, neo4j_driver

students_data = [
    {
        "name": "Alice",
        "email": "alice@example.com",
        "skills": ["Python", "Data Science"],
        "enrolled_courses": ["C101", "C103"]
    },
    {
        "name": "Bob",
        "email": "bob@example.com",
        "skills": ["Java", "Web Development"],
        "enrolled_courses": ["C102"]
    }
]

courses_data = [
    {
        "course_id": "C101",
        "title": "Introduction to Python",
        "category": "Programming",
        "skills_covered": ["Python"]
    },
    {
        "course_id": "C102",
        "title": "Web Development Basics",
        "category": "Web",
        "skills_covered": ["HTML", "CSS", "JavaScript"]
    },
    {
        "course_id": "C103",
        "title": "Data Science 101",
        "category": "AI/ML",
        "skills_covered": ["Python", "Data Science"]
    }
]

mongo_db.Students.insert_many(students_data)
mongo_db.Courses.insert_many(courses_data)
print("Data inserted into MongoDB successfully.")

with neo4j_driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")
    print("Cleared existing Neo4j data.")

    # Created nodes and relationships
    for student in students_data:
        session.run(
            """
            CREATE (s:Student {name: $name, email: $email})
            """, name=student["name"], email=student["email"]
        )
        for skill in student["skills"]:
            session.run("MERGE (sk:Skill {name: $skill})", skill=skill)
            session.run(
                """
                MATCH (s:Student {name: $student_name}), (sk:Skill {name: $skill})
                MERGE (s)-[:HAS_SKILL]->(sk)
                """,
                student_name=student["name"],
                skill=skill
            )

        for course_id in student["enrolled_courses"]:
            course = next((c for c in courses_data if c["course_id"] == course_id), None)
            if course:
                session.run(
                    """
                    MERGE (c:Course {course_id: $course_id, title: $title})
                    """,
                    course_id=course["course_id"],
                    title=course["title"]
                )
                session.run(
                    """
                    MATCH (s:Student {name: $student_name}), (c:Course {course_id: $course_id})
                    MERGE (s)-[:ENROLLED_IN]->(c)
                    """,
                    student_name=student["name"],
                    course_id=course["course_id"]
                )

    # Linked courses to required skills
    for course in courses_data:
        for skill in course["skills_covered"]:
            session.run("MERGE (sk:Skill {name: $skill})", skill=skill)
            session.run(
                """
                MATCH (c:Course {course_id: $course_id}), (sk:Skill {name: $skill})
                MERGE (c)-[:REQUIRES_SKILL]->(sk)
                """,
                course_id=course["course_id"],
                skill=skill
            )

    print("Data inserted into Neo4j successfully.")

neo4j_driver.close()

# app/functions.py
# --- TEMPORARY HARDCODED SAMPLE DATA for testing Streamlit frontend ---

def get_all_students():
    """Return a list of mock students"""
    return [
        {"name": "Ashwini", "email": "ashwini@example.com"},
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
        {"name": "Charlie", "email": "charlie@example.com"},
    ]


def get_student_graph_data(student_name):
    """Return mock skills and enrolled courses"""
    data = {
        "Ashwini": {
            "skills": ["Python", "Data Analysis"],
            "courses": ["Intro to Python", "Data Visualization 101"]
        },
        "Alice": {
            "skills": ["C++", "Data Engineering"],
            "courses": ["Intro to C++", "Data Modelling"]
        },
        "Bob": {
            "skills": ["HTML", "CSS"],
            "courses": ["Web Design Basics"]
        },
        "Charlie": {
            "skills": ["Java", "SQL"],
            "courses": ["Database Fundamentals"]
        }
    }
    return data.get(student_name, {"skills": [], "courses": []})


def recommend_courses(student_name):
    """Return sample recommendations, as if from Neo4j + Redis"""
    sample_recommendations = {
        "Ashwini": ["Advanced Python", "Data Science Essentials"],
        "Alice": ["Advanced C++", "Machine Learning Essentials"],
        "Bob": ["JavaScript for Beginners", "Responsive Web Design"],
        "Charlie": ["Advanced SQL", "Spring Boot Basics"]
    }
    return sample_recommendations.get(student_name, [])

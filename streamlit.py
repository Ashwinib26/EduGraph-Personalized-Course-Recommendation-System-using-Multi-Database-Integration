import streamlit as st
from app.recommendations import get_recommendations

st.set_page_config(page_title="EduGraph - Course Recommendation", layout="centered")

st.title("🎓 EduGraph: Smart Course Recommendation System")

student_id = st.number_input("Enter Student ID:", min_value=1, step=1)

if st.button("Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        recs = get_recommendations(int(student_id))
        if recs:
            st.success("Recommended Courses:")
            for c in recs:
                st.write(f"• {c}")
        else:
            st.warning("No recommendations found.")

import streamlit as st
from app.functions import get_all_students, get_student_graph_data, recommend_courses

st.set_page_config(page_title="EduGraph", page_icon="📊", layout="centered")
st.title("🎓 EduGraph — Student Learning Graph")

students = get_all_students()
student_names = [s["name"] for s in students]

selected = st.selectbox("Select a Student:", student_names)

if selected:
    graph_data = get_student_graph_data(selected)
    st.subheader(f"👤 {selected}'s Profile")
    st.write(f"**Skills:** {', '.join(graph_data['skills']) if graph_data['skills'] else 'None'}")
    st.write(f"**Enrolled Courses:** {', '.join(graph_data['courses']) if graph_data['courses'] else 'None'}")

    st.divider()

    if st.button("📘 Recommend Courses"):
        recommended = recommend_courses(selected)
        if recommended:
            st.success(f"Recommended Courses for {selected}:")
            st.write(", ".join(recommended))
        else:
            st.info("No new recommendations — student already enrolled in all relevant courses.")

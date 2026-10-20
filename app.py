import streamlit as st
import csv

st.set_page_config(
    page_title="CareerPath AI",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 CareerPath AI")
st.subheader("Your future after Class 12")

st.write(
    "Explore courses, check eligibility, and discover "
    "future career opportunities."
)

st.info(
    "This is the student information form. "
    "Verified course eligibility checking comes next."
)

with st.form("student_form"):

    name = st.text_input("Student name")

    board = st.selectbox(
        "Class 12 education board",
        [
            "CBSE",
            "ISC",
            "Karnataka State Board",
            "Tamil Nadu State Board",
            "Other"
        ]
    )

    stream = st.selectbox(
        "Select your stream",
        [
            "Science - PCM",
            "Science - PCB",
            "Science - PCMB",
            "Commerce",
            "Arts / Humanities",
            "Other"
        ]
    )

    subject_options = {
        "Science - PCM": [
            "English", "Physics", "Chemistry", "Mathematics",
            "Computer Science", "Other"
        ],
        "Science - PCB": [
            "English", "Physics", "Chemistry", "Biology",
            "Mathematics", "Other"
        ],
        "Science - PCMB": [
            "English", "Physics", "Chemistry", "Mathematics",
            "Biology", "Computer Science", "Other"
        ],
        "Commerce": [
            "English", "Accountancy", "Business Studies",
            "Economics", "Mathematics", "Computer Science", "Other"
        ],
        "Arts / Humanities": [
            "English", "History", "Political Science",
            "Geography", "Economics", "Psychology", "Other"
        ],
        "Other": [
            "English", "Mathematics", "Science",
            "Commerce", "Other"
        ]
    }

    subjects = st.multiselect(
        "Select all your subjects",
        subject_options[stream]
    )

    st.write("### Subject marks (%)")
    st.caption("Enter each subject's percentage from 0 to 100.")

    marks = {}

    for subject in subjects:
        marks[subject] = st.number_input(
            f"{subject} marks (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=1.0,
            key=f"mark_{subject}"
        )

    interests = st.multiselect(
        "What are your career interests?",
        [
            "Technology and computers",
            "Healthcare and biology",
            "Business and management",
            "Finance and accounting",
            "Engineering",
            "Arts and design",
            "Law and public service",
            "Teaching and research",
            "Not sure yet"
        ]
    )

    submitted = st.form_submit_button(
        "Explore my career options"
    )

if submitted:

    if not name.strip():
        st.error("Please enter your name.")

    elif not subjects:
        st.error("Please select your Class 12 subjects.")

    elif not interests:
        st.error("Please select at least one career interest.")

    else:
        st.success(f"Welcome, {name}!")

        st.write("**Education board:**", board)
        st.write("**Stream:**", stream)
        st.write("**Your subjects and marks:**")

        for subject, mark in marks.items():
            st.write(f"- {subject}: {mark}%")

        if marks:
            average = sum(marks.values()) / len(marks)
            st.write(f"**Average of entered subject percentages:** {average:.1f}%")

        st.write("**Your interests:**", ", ".join(interests))
        st.subheader("📚 Course pathways to explore")

        try:
            with open(
                "career_database.csv",
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as file:
                reader = csv.DictReader(file)
                courses = list(reader)

            matching_courses = [
                course for course in courses
                if course.get("stream", "").strip() == stream
            ]

            if matching_courses:
                for course in matching_courses:
                    st.markdown(
                        f"### {course.get('course_name', 'Unnamed course')}"
                    )

                    st.write(
                        "**Subjects to check:**",
                        course.get("required_subjects", "")
                        or "Not yet specified"
                    )

                    st.write(
                        "**Entrance exams:**",
                        course.get("entrance_exams", "").strip()
                        or "Check the official institution's admission requirements"
                    )

                    st.write(
                        "**Possible career pathways:**",
                        course.get("career_paths", "")
                        or "Not yet specified"
                    )

                    st.info(
                        "This is a possible pathway, not a confirmed "
                        "eligibility decision. Verify requirements "
                        "with the official institution."
                    )

                    source = (
                        course.get("official_source_url") or ""
                    ).strip()

                    if source.startswith(("https://", "http://")):
                        st.markdown(
                            f"[Check official course information]({source})"
                        )

                    st.divider()
            else:
                st.info(
                    "No starter pathways are listed for this stream yet."
                )

        except FileNotFoundError:
            st.error(
                "career_database.csv was not found. "
                "Save it inside your CareerPathAI project folder."
            )

        except (KeyError, csv.Error) as error:
            st.error(
                f"Please check the CSV column headings and data: {error}"
            )
# -------------------------------
# CareerPath AI - Groq Chat Guide
# -------------------------------

import os
from groq import Groq

st.divider()
st.header("🤖 Ask CareerPath AI")
st.write(
    "Ask questions in English about courses, "
    "Class 12 subjects, entrance exams, and career options."
)

# Read the existing course database
try:
    with open(
        "career_database.csv",
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)
        all_courses = list(reader)

    course_context = "\n".join(
    f"Stream: {c.get('stream', '')}; "
    f"Course: {c.get('course_name', '')}; "
    f"Required subjects: {c.get('required_subjects', '')}; "
    f"Minimum marks: {c.get('min_marks', '')}; "
    f"Entrance exams: {c.get('entrance_exams', '')}; "
    f"Duration: {c.get('duration', '')}; "
    f"Career paths: {c.get('career_paths', '')}; "
    f"Eligibility notes: {c.get('eligibility_notes', '')}; "
    f"Verification status: {c.get('verification_status', '')}; "
    f"Official source: {c.get('official_source_url', '')}"
    for c in all_courses
   )

except (OSError, csv.Error):
    course_context = "The course database is currently unavailable."

# Keep the conversation during Streamlit reruns
if "career_chat_messages" not in st.session_state:
    st.session_state.career_chat_messages = []

# Display previous messages
for message in st.session_state.career_chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask about your career options..."
)

if question:
    st.session_state.career_chat_messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error(
            "Groq API key not found. Check your Windows "
            "GROQ_API_KEY environment variable, then restart "
            "your terminal and Streamlit."
        )

    else:
        try:
            client = Groq(api_key=api_key)

            # Keep recent conversation history
            recent_messages = (
                st.session_state.career_chat_messages[-10:]
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are CareerPath AI, a friendly career guidance "
                        "assistant for Indian Class 12 students. Use simple English. "
                        "Use the supplied course database as your primary source. "
                        "For each recommended course, use these headings:\n"
                        "### Course\n"
                        "### What you study\n"
                        "### Why it fits\n"
                        "### Entrance exams\n"
                        "### Eligibility and required subjects\n"
                        "### Career paths you could aim for\n"
                        "### Official source\n\n"
                        "Use the matching course record to fill every section. "
                        "Use required_subjects, min_marks, and eligibility_notes "
                        "for eligibility guidance. Use entrance_exams for exams, "
                        "career_paths for career options, and official_source_url "
                        "for the official source link. Never leave a section blank. "
                        "If a field is missing, say it is not available in the database. "
                        "Do not invent admission rules or guarantee eligibility. "
                        "Respect verification_status and advise students to verify "
                        "requirements with the official institution.\n\n"
                        "COURSE DATABASE:\n"
                        + course_context[:18000]
                    )
                }
            ] + recent_messages

            with st.chat_message("assistant"):
                with st.spinner("Preparing your career guidance..."):
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=messages,
                        max_completion_tokens=500
                    )

                    answer = response.choices[0].message.content
                    if not answer:
                        answer = (
                            "I couldn't generate an answer. "
                            "Please try asking another way."
                        )

                    st.markdown(answer)

            st.session_state.career_chat_messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            st.error(
                "The AI request failed. Please check your "
                "internet connection, Groq model access, "
                "API usage limits, and API key configuration."
            )
            st.caption(f"Technical details: {type(error).__name__}")
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="ExamPrep AI Assistant",
    page_icon="📚",
    layout="wide"
)

# ---------------- API KEY ----------------
load_dotenv()

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Add it in .env locally or Streamlit Secrets during deployment.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ---------------- UI ----------------
st.title("📚 ExamPrep AI Assistant")
st.write("Only for exam preparation, study plans, quizzes, interview preparation, and technical learning.")

question = st.text_area("Ask your exam or study-related question")

# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
You are ExamPrep AI Assistant.

Your job is ONLY to help students with:
- Exam preparation
- Study plans
- Time management
- Important questions
- Quiz generation
- Mock tests
- Interview preparation
- Technical learning
- School, Intermediate, Degree, B.Tech subjects
- Python, AI, ML, SQL, Automation Testing, Web Development, Data Science

Strict Rules:
1. Answer ONLY study, exam, education, interview, and technical-learning questions.
2. If the user asks unrelated topics like food, biryani, movies, travel, shopping, entertainment, sports, or personal matters, reply only:
"I am ExamPrep AI Assistant. Please ask exam or study-related questions only."
3. Answer exactly what the user asks.
4. If user asks for 1 hour plan, give exactly 1 hour plan.
5. If user asks for 2 hours plan, give exactly 2 hours plan.
6. If user asks for 30 days plan, give exactly 30 days plan.
7. If user asks for quiz, generate quiz only.
8. If user asks for important questions, give important questions only.
9. If user asks definition, give definition only.
10. Keep answers short, clear, and student-friendly.
11. Do not give extra matter.
"""

# ---------------- BUTTON ----------------
if st.button("Get Answer"):
    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=700
            )

            answer = response.choices[0].message.content
            st.success("Answer Generated ✅")
            st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")

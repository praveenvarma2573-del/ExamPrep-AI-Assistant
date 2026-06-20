import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Check your .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(
    page_title="ExamPrep AI Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 ExamPrep AI Assistant")
st.write("Only for exam preparation, study plans, quizzes, interview preparation, and technical learning.")

question = st.text_area("Ask your exam or study-related question")

system_prompt = """
You are ExamPrep AI Assistant.

Answer only exam, study, education, interview, and technical-learning questions.

If the user asks unrelated topics like food, biryani, movies, travel, shopping, entertainment, sports, or personal matters, reply only:
"I am ExamPrep AI Assistant. Please ask exam or study-related questions only."

Answer exactly what the user asks.
If user asks for 1 hour plan, give exactly 1 hour plan.
If user asks for 2 hours plan, give exactly 2 hours plan.
If user asks for quiz, generate quiz only.
If user asks for important questions, give important questions only.
Keep answers short, clear, and student-friendly.
Do not give extra matter.
"""

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

            st.success("Answer Generated ✅")
            st.write(response.choices[0].message.content)

        except Exception as e:
            if "401" in str(e):
                st.error("Invalid Groq API key. Create a new key and paste it in .env correctly.")
            else:
                st.error(f"Error: {e}")
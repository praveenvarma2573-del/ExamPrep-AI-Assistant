import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in .env")
    st.stop()

client = Groq(api_key=api_key)

st.title("🤖 ExamPrep Chatbot Agent")

agent = st.selectbox(
    "Select Agent",
    [
        "Study Plan Agent",
        "Quiz Agent",
        "Important Questions Agent",
        "Technical Learning Agent"
    ]
)

question = st.text_area("Ask your question")

system_prompt = f"""
You are {agent}.

Answer only exam, study, education, and technical learning questions.
Do not answer unrelated topics.

If unrelated, reply:
"I am ExamPrep Agent. Please ask exam or study-related questions only."

Give answer based on selected agent.
"""

if st.button("Run Agent"):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    st.write(response.choices[0].message.content)
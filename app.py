import streamlit as st

import google.generativeai as genai

import sqlite3

import os

from datetime import datetime

from pypdf import PdfReader

from reportlab.pdfgen import canvas



# ---------------- CONFIG ----------------

API_KEY = "AQ.Ab8RN6I0xVpzPZeog4ud5QxvQ3EY0c-HULN0B93NqNr52fVVcw" 

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")



os.makedirs("uploads", exist_ok=True)

os.makedirs("history", exist_ok=True)

os.makedirs("database", exist_ok=True)



# ---------------- DATABASE ----------------

conn = sqlite3.connect("database/chat_history.db", check_same_thread=False)

cursor = conn.cursor()



cursor.execute("""

CREATE TABLE IF NOT EXISTS chats (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    question TEXT,

    answer TEXT,

    created_at TEXT

)

""")

conn.commit()



# ---------------- PAGE ----------------

st.set_page_config(

    page_title="ExamPrep AI Assistant",

    page_icon="📚",

    layout="wide"

)



st.title("📚 ExamPrep AI Assistant")

st.write("AI Chatbot + Study Plan + Quiz + PDF Notes + RAG + Chat History")



# ---------------- SIDEBAR ----------------

st.sidebar.title("📌 ExamPrep Menu")



mode = st.sidebar.selectbox(

    "Choose Feature",

    [

        "AI Chatbot",

        "Study Plan Generator",

        "Quiz Generator",

        "Interview Preparation",

        "PDF Notes Q&A",

        "Chat History"

    ]

)



subject = st.sidebar.selectbox(

    "Choose Subject",

    [

        "General",

        "Python",

        "AI",

        "Machine Learning",

        "SQL",

        "Automation Testing",

        "Web Development",

        "Data Science"

    ]

)



dark_mode = st.sidebar.checkbox("🌙 Dark Mode")



if dark_mode:

    st.markdown("""

    <style>

    .stApp {

        background-color: #111827;

        color: white;

    }

    </style>

    """, unsafe_allow_html=True)



# ---------------- HELPER FUNCTIONS ----------------

def ask_gemini(prompt):

    response = model.generate_content(prompt)

    return response.text



def save_chat(question, answer):

    cursor.execute(

        "INSERT INTO chats (question, answer, created_at) VALUES (?, ?, ?)",

        (question, answer, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    )

    conn.commit()



def create_pdf(text, filename):

    path = f"history/{filename}"

    c = canvas.Canvas(path)

    width, height = 595, 842



    y = height - 40

    for line in text.split("\n"):

        if y < 40:

            c.showPage()

            y = height - 40

        c.drawString(40, y, line[:95])

        y -= 18



    c.save()

    return path



def read_pdf(uploaded_file):

    pdf_path = os.path.join("uploads", uploaded_file.name)



    with open(pdf_path, "wb") as f:

        f.write(uploaded_file.getbuffer())



    reader = PdfReader(pdf_path)

    text = ""



    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"



    return text



# ---------------- AI CHATBOT ----------------

if mode == "AI Chatbot":

    st.header("🤖 AI Chatbot")



    question = st.text_area("Ask your study-related question")



    if st.button("Get Answer"):

        if question.strip() == "":

            st.warning("Please enter a question")

        else:

            prompt = f"""

            You are an Exam Preparation Assistant.



            Subject: {subject}



            Explain in simple student-friendly language.

            Give examples and exam tips.



            Question:

            {question}

            """



            answer = ask_gemini(prompt)

            st.success("Answer Generated ✅")

            st.write(answer)



            save_chat(question, answer)



            pdf_path = create_pdf(answer, "answer.pdf")

            with open(pdf_path, "rb") as file:

                st.download_button(

                    "⬇️ Download Answer as PDF",

                    file,

                    file_name="answer.pdf"

                )



# ---------------- STUDY PLAN ----------------

elif mode == "Study Plan Generator":

    st.header("📅 Study Plan Generator")



    exam_name = st.text_input("Enter exam/subject name")

    days = st.number_input("How many days plan?", min_value=1, max_value=100, value=7)



    if st.button("Generate Study Plan"):

        prompt = f"""

        Create a {days}-day study plan for {exam_name}.

        Include daily topics, revision time, practice questions, and exam tips.

        """



        answer = ask_gemini(prompt)

        st.write(answer)

        save_chat(f"Study Plan: {exam_name}", answer)



# ---------------- QUIZ GENERATOR ----------------

elif mode == "Quiz Generator":

    st.header("📝 Quiz Generator")



    topic = st.text_input("Enter quiz topic")

    count = st.number_input("Number of questions", min_value=5, max_value=50, value=10)



    if st.button("Generate Quiz"):

        prompt = f"""

        Generate {count} quiz questions on {topic}.

        Include 4 options and correct answer.

        """



        answer = ask_gemini(prompt)

        st.write(answer)

        save_chat(f"Quiz: {topic}", answer)



# ---------------- INTERVIEW PREPARATION ----------------

elif mode == "Interview Preparation":

    st.header("🎤 Interview Preparation")



    role = st.text_input("Enter job role", value="Automation Testing Engineer")



    if st.button("Generate Interview Questions"):

        prompt = f"""

        Generate interview preparation content for {role}.

        Include:

        - Self introduction

        - Top 20 interview questions

        - Answers

        - Technical topics

        - Final interview tips

        """



        answer = ask_gemini(prompt)

        st.write(answer)

        save_chat(f"Interview Prep: {role}", answer)



# ---------------- PDF NOTES Q&A ----------------

elif mode == "PDF Notes Q&A":

    st.header("📄 Upload PDF Notes and Ask Questions")



    uploaded_file = st.file_uploader("Upload PDF Notes", type=["pdf"])



    if uploaded_file:

        pdf_text = read_pdf(uploaded_file)

        st.success("PDF uploaded and text extracted ✅")



        question = st.text_area("Ask question from PDF")



        if st.button("Ask from PDF"):

            prompt = f"""

            Answer the question using the PDF notes below.



            PDF Notes:

            {pdf_text[:12000]}



            Question:

            {question}



            Give answer in simple language.

            """



            answer = ask_gemini(prompt)

            st.write(answer)

            save_chat(f"PDF Question: {question}", answer)



# ---------------- CHAT HISTORY ----------------

elif mode == "Chat History":

    st.header("🕘 Chat History")



    cursor.execute("SELECT question, answer, created_at FROM chats ORDER BY id DESC")

    rows = cursor.fetchall()



    if len(rows) == 0:

        st.info("No chat history found")

    else:

        for q, a, t in rows:

            st.markdown(f"### 🕒 {t}")

            st.write("**Question:**", q)

            st.write("**Answer:**", a)

            st.markdown("---")



        if st.button("Clear Chat History"):

            cursor.execute("DELETE FROM chats")

            conn.commit()

            st.success("Chat history cleared. Refresh page.")
import streamlit as st
import openai
import re

# Set your OpenAI API key here or better: set environment variable OPENAI_API_KEY and use `openai.api_key = os.getenv("OPENAI_API_KEY")`
openai.api_key = "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"

def defang_url(url):
    return url.replace('.', '[.]').replace(':', '[:]')

def sanitize_message(message):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.sub(lambda m: defang_url(m.group(0)), message)

def ask_openai_chat(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Or "gpt-4", "gpt-3.5-turbo" as available
        messages=[
            {"role": "system", "content": "You are a helpful math tutor."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content

# Initialize chat message history in session state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"sender": "bot", "text": "Hi! Ask me anything about the lesson."}
    ]

def add_chat_message(sender, text):
    st.session_state.chat_messages.append({"sender": sender, "text": text})

st.title("Personalized LMS with AI Chat")

# Lesson content
lesson_text = """
# Basic Algebra Lesson

In this lesson, you will learn how to solve simple linear equations.

Example: Solve for x: 2x + 3 = 7
"""

st.markdown(lesson_text)

# Practice problem
practice_question = "Solve for x: 2x + 3 = 7"
correct_answer = "2"

st.subheader("Practice Problem")
st.write(practice_question)
user_answer = st.text_input("Your answer:")

if st.button("Submit Answer"):
    if user_answer.strip() == correct_answer:
        st.success("Correct! Well done.")
    else:
        st.error(f"Oops! The correct answer is {correct_answer}.")

# Chat interface
st.subheader("Chat with Tutor")

for msg in st.session_state.chat_messages:
    if msg["sender"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Tutor:** {msg['text']}")

user_input = st.text_input("Type your question:")

if st.button("Send"):
    if user_input.strip():
        sanitized = sanitize_message(user_input)
        add_chat_message("user", sanitized)

        with st.spinner("Thinking..."):
            bot_response = ask_openai_chat(sanitized)

        add_chat_message("bot", bot_response)
        from streamlit.runtime import scriptrunner
        from streamlit.runtime.scriptrunner import RerunData

        raise scriptrunner.RerunException(RerunData())

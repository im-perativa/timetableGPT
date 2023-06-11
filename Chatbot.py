import streamlit as st
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from streamlit_chat import message

prompt_template = """
The documents is a timetable with information of what time a person and a room will be occupied. 
Outside of the data stored in timetable, it is assumed that a person and room is free. 
A user cannot use the room if the room is occupied.
A user also cannot schedule a meeting with a person if the person is occupied.

You can use the following context to help answer the user question.

{context}

Question: {question}
Answer:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key")
    "[View the source code](https://github.com/im-perativa/timetableGPT/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/im-perativa/timetableGPT?quickstart=1)"

st.title("📆 Timetable GPT")

st.session_state

if "texts" in st.session_state:
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    docsearch = Chroma.from_documents(st.session_state["texts"], embeddings)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="What would you like to say?",
        label_visibility="collapsed",
    )
    b.form_submit_button("Send", use_container_width=True)

for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")

if user_input and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")


def generate_response(input_text):
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=openai_api_key),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT},
    )
    return qa.run(input_text)


if user_input and openai_api_key:
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    response = generate_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    message(response)

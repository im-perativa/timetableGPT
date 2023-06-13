import streamlit as st
from langchain import OpenAI
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.vectorstores import Chroma
from streamlit_chat import message

_template = """
You are an assistant to help user with a Timetable document.
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question in user language:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """
You are an assistant to help user with a Timetable document. 
The timetable document contains information of what time a person and a room will be occupied.
Outside of the information stored in timetable, it is assumed that a person and room is free.
You cannot use the room at specific time if the room is occupied at the same time.
You cannot schedule a meeting with a person at specific time if the person is occupied at the same time.
If the question is not the Timetable document, politely inform them that you are tuned to only answer questions about Timetable.
Question: {question}
=========
{context}
=========
Answer in user language:
"""

QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key")
    "[View the source code](https://github.com/im-perativa/timetableGPT/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/im-perativa/timetableGPT?quickstart=1)"

st.title("📆 Timetable GPT")

st.session_state

if "texts" in st.session_state:
    embeddings = OpenAIEmbeddings(client="timetableGPT", openai_api_key=openai_api_key)
    docsearch = Chroma.from_documents(st.session_state["texts"], embeddings)
else:
    st.error("Please input your Timetable first")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="What would you like to say?",
        label_visibility="collapsed",
    )
    b.form_submit_button("Send", use_container_width=True)

for msg in st.session_state["messages"]:
    message(msg["content"], is_user=msg["role"] == "user")

if user_input and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")


def generate_response(input_text, chat_history):
    qa = ConversationalRetrievalChain.from_llm(
        llm=OpenAI(
            client="timetableGPT",
            openai_api_key=openai_api_key,
        ),
        retriever=docsearch.as_retriever(),
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        memory=ConversationBufferMemory(
            memory_key="chat_history",
            input_key="question",
            output_key="answer",
            return_messages=True,
        ),
        chain_type="stuff",
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        verbose=True,
    )
    return qa({"question": input_text, "chat_history": chat_history})


if user_input and openai_api_key:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    response = generate_response(user_input, st.session_state["chat_history"])
    st.session_state["chat_history"].append(response["chat_history"])
    st.session_state["messages"].append(
        {"role": "assistant", "content": response["answer"]}
    )
    message(response["answer"])

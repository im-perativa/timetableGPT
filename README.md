# 📆TimetableGPT

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/im-perativa/timetableGPT?quickstart=1)

📆TimetableGPT use the power of LLM to allow you to ask questions about your timetable and get accurate answers to help you manage it so that no schedule will overlap each other. 
The Timetable consists of four columns:  
1. `person`: information about PERSON name
2. `datetime_start`: information about date and time for the start of a PERSON schedule
3. `datetime_end`: information about date and time for the end of a PERSON schedule
4. `room`: information about what ROOM a PERSON use for their scheduled agenda

## ❔Example questions you can ask

- List all unoccupied room on February, 6th 2023 from 10am to 12pm
- Can I use `Room x` on February, 6th 2023 from 1.00 pm for 31 minutes?
- What is the best time to arrange a 1 hour meeting between `Person A`, `Person B` and `Person C` on February, 6th 2023? 
- List all schedule of `Person A` on February, 6th 2023
- etc

## 🌏Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://timetablegpt.streamlit.app/)

## 💻Run the App Locally

1. Clone the repository📂

```bash
git clone https://github.com/im-perativa/timetableGPT
cd timetableGPT
```

2. Install dependencies with pip⚙️

```bash
pip install -r requirements.txt
```

3. Run the Streamlit server🚀

```bash
streamlit run Chatbot.py
```

## 🗝️Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

Please note that free trial users are limited to 3 request per minute as [specified](https://platform.openai.com/docs/guides/rate-limits/overview) by OpenAI.
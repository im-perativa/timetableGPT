import pandas as pd
import streamlit as st
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import CharacterTextSplitter


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


uploaded_file = st.file_uploader(
    "Choose an Excel file", type=[".xlsx", ".xls"], key="uploaded_file"
)

st.session_state["uploaded_file"]

if uploaded_file is not None:
    dataframe = pd.read_excel(
        uploaded_file, parse_dates=["datetime_start", "datetime_end"]
    )

    timetable = st.data_editor(
        dataframe,
        column_config={
            "datetime_start": st.column_config.DatetimeColumn(
                label="Date Start", format="D MMM YYYY, h:mm a", step=60, required=True
            ),
            "datetime_end": st.column_config.DatetimeColumn(
                label="Date End", format="D MMM YYYY, h:mm a", step=60, required=True
            ),
            "person": st.column_config.TextColumn(
                label="Person", max_chars="50", required=True
            ),
            "room": st.column_config.TextColumn(
                label="Room", max_chars="50", required=True
            ),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
    )

    timetable["prompt"] = (
        timetable["person"]
        + " and room "
        + timetable["room"]
        + " is occupied from "
        + timetable["datetime_start"].astype(str)
        + " to "
        + timetable["datetime_end"].astype(str)
    )

    loader = DataFrameLoader(timetable[["prompt"]], page_content_column="prompt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    st.session_state["timetable"] = timetable
    st.session_state["texts"] = texts

elif "timetable" in st.session_state:
    timetable = st.data_editor(
        st.session_state["timetable"],
        column_config={
            "datetime_start": st.column_config.DatetimeColumn(
                label="Date Start", format="D MMM YYYY, h:mm a", step=60, required=True
            ),
            "datetime_end": st.column_config.DatetimeColumn(
                label="Date End", format="D MMM YYYY, h:mm a", step=60, required=True
            ),
            "person": st.column_config.TextColumn(
                label="Person", max_chars="50", required=True
            ),
            "room": st.column_config.TextColumn(
                label="Room", max_chars="50", required=True
            ),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
    )

    st.session_state["timetable"] = timetable

if "timetable" in st.session_state:
    csv = convert_df(timetable)

    st.download_button(
        "Press to Download", csv, "file.csv", "text/csv", key="download-csv"
    )

import pandas as pd
import streamlit as st


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


with st.sidebar:
    "[Download sample file](https://github.com/im-perativa/timetableGPT/blob/main/sample.xlsx)"

uploaded_file = st.file_uploader(
    "Choose an Excel file", type=[".xlsx", ".xls"], key="uploaded_file"
)

# dataframe = pd.DataFrame(columns=["person", "datetime_start", "datetime_end", "room"])
dataframe = pd.read_excel("sample.xlsx", parse_dates=["datetime_start", "datetime_end"])

if uploaded_file is not None:
    dataframe = pd.read_excel(
        uploaded_file, parse_dates=["datetime_start", "datetime_end"]
    )
elif "timetable" in st.session_state:
    dataframe = st.session_state["timetable"][
        ["person", "datetime_start", "datetime_end", "room"]
    ]

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
            label="Person", max_chars=50, required=True
        ),
        "room": st.column_config.TextColumn(label="Room", max_chars=50, required=True),
    },
    hide_index=True,
    use_container_width=True,
    num_rows="dynamic",
)

st.session_state["timetable"] = timetable

if "timetable" in st.session_state:
    csv = convert_df(st.session_state["timetable"])

    st.download_button(
        "Press to Download", csv, "file.csv", "text/csv", key="download-csv"
    )

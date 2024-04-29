import json
import datetime
import tempfile
from typing import Any, Dict, List, Tuple
import streamlit as st


from transcriber import Transcriber


def parse_transcription_output(
    json_data: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    params = json_data["params"]
    rows = [
        {"text": row["text"].strip()} | row["timestamps"]
        for row in json_data["transcription"]
    ]
    return rows, params


def main():
    st.title("Transcription app")

    uploaded_file = st.file_uploader(
        "Upload an audio file", type=["mp3", "wav", "ogg", "m4a", "aac"]
    )

    if uploaded_file is not None:
        with st.spinner("Wait for it..."):
            data = process_audio_file(uploaded_file)
            rows, params = parse_transcription_output(json.loads(data))
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Model", value=params["model"])
                st.metric(label="Language", value=params["language"])
            with col2:
                st.audio(
                    uploaded_file, format="audio/" + uploaded_file.name.split(".")[-1]
                )
                with st.popover("Listen to audio snippets 🔊"):
                    for row in rows:
                        with st.expander(f"Text: {row['text']}"):
                            start_time = as_timedelta(row["from"])
                            end_time = as_timedelta(row["to"])
                            st.audio(
                                uploaded_file, start_time=start_time, end_time=end_time
                            )

            st.dataframe(rows)


def as_timedelta(timestamp: str) -> datetime.timedelta:
    time_delta = datetime.timedelta(
        hours=int(timestamp[0:2]),
        minutes=int(timestamp[3:5]),
        seconds=int(timestamp[6:8]),
        microseconds=int(timestamp[9:]),
    )
    return time_delta


@st.cache_data
def process_audio_file(uploaded_file: bytes):
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        transcriber = Transcriber(audio_path=temp_file.name)
        data = transcriber.whisper_model.json
        return data


if __name__ == "__main__":
    main()

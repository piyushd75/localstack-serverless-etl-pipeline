import streamlit as st

from services.file_service import (
    save_uploaded_file,
)

st.set_page_config(
    page_title="Sales ETL Pipeline",
    page_icon="📊",
)

st.title(
    "📊 Sales ETL Pipeline"
)

uploaded_file = st.file_uploader(
    "Upload Sales CSV",
    type=["csv"],
)

if uploaded_file:

    st.success(
        f"Selected: {uploaded_file.name}"
    )

    if st.button(
        "Upload File"
    ):

        try:

            file_name = (
                save_uploaded_file(
                    uploaded_file
                )
            )

            st.success(
                f"{file_name} uploaded successfully."
            )

            st.info(
                "Go to Airflow UI and trigger the DAG using the filename."
            )

        except Exception as e:

            st.error(
                f"Upload failed: {e}"
            )
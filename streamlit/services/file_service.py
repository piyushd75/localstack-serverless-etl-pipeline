import os
import shutil
from pathlib import Path


IS_DOCKER = os.path.exists(
    "/.dockerenv"
)

if IS_DOCKER:
    STREAMLIT_UPLOAD_DIR = Path(
        "/app/uploads"
    )

    AIRFLOW_UPLOAD_DIR = Path(
        "/app/uploads"
    )

else:
    STREAMLIT_UPLOAD_DIR = Path(
        "streamlit/uploads"
    )

    AIRFLOW_UPLOAD_DIR = Path(
        "airflow/include/uploads"
    )


def save_uploaded_file(
    uploaded_file,
):
    file_name = (
        uploaded_file.name
    )

    STREAMLIT_UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    streamlit_file_path = (
        STREAMLIT_UPLOAD_DIR /
        file_name
    )

    with open(
        streamlit_file_path,
        "wb",
    ) as f:
        f.write(
            uploaded_file.getbuffer()
        )

    if not IS_DOCKER:

        AIRFLOW_UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        airflow_file_path = (
            AIRFLOW_UPLOAD_DIR /
            file_name
        )

        shutil.copy(
            streamlit_file_path,
            airflow_file_path,
        )

    return file_name
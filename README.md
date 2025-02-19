# Geobench

This is a demonstration of FastAPI and Streamlit for my UU programming cafe presentation 6 March 2025. 

*****

This project has three components:

1. A FastAPI rest server to handle ingesting data, and sending data to clients
2. A Streamlit upload interface to take .zip archives of ProPAT v16 or v17 benchmark results
3. A Streamlit viewer app with a Plotly boxplot to visualize the results of the .zip archives.

*****

You can start the FastAPI server with:

`uvicorn api_server:app`

*****

You can start the Streamlit Upload App with:

`streamlit run upload_app/upload_app.py`

***** 

You can start the Streamlit Viewer App with:

`streamlit run viewer_app/viewer.py`
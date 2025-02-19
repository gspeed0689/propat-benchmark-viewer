import results_v16 as r16
import results_v17 as r17
import pandas as pd
import streamlit as st
import zipfile
import requests
from io import StringIO
import json

api_base = "http://localhost:8000/api"

st.title("ProPAT Benchmark Upload")

upload_zip = st.file_uploader("Upload a zip package of the results.",
                              type=["zip", ".zip"])

if upload_zip:
    request_computers = requests.get(f"{api_base}/get-computers")
    request_storage = requests.get(f"{api_base}/get-storage")

    existing_computers = json.loads(request_computers.content)
    existing_storage = json.loads(request_storage.content)

    existing_computers = existing_computers["items"] + ["Other"]
    existing_storage = existing_storage["items"] + ["Other"]

    computer_name = st.selectbox("Computer Name", existing_computers)
    storage_name = st.selectbox("Storage Name", existing_storage)

    if computer_name == "Other":
        other_computer_name = st.text_input("Other computer name")
    if storage_name == "Other":
        other_storage_name = st.text_input("Other storage name")
    bench_version = st.segmented_control("ProPAT Version", [16, 17])

def decode_timecode(timecode):
    ts = timecode.split(":")
    # print(ts)
    h, m, s = int(ts[0]), int(ts[1]), float(ts[2])
    total = (h * 60 * 60) + (m * 60) + s
    return(total)

def send_result(bname, btime):
    if computer_name == "Other":
        transmit_computer_name = other_computer_name
    else:
        transmit_computer_name = computer_name
    if storage_name == "Other":
        transmit_storage_name = other_storage_name
    else:
        transmit_storage_name = storage_name
    
    result_data = {
        "benchmark_name": bname,
        "benchmark_elapsed_time": btime,
        "computer_name": transmit_computer_name,
        "storage_name": transmit_storage_name, 
        "benchmark_version": bench_version
    }
    requests.post(f"{api_base}/add-result", json=result_data)

def send_results():
    for result in results.keys():
        if type(results[result]) == float:
            benchmark_name = result
            if "FPS" in benchmark_name:
                continue
            else:
                benchmark_time = results[result]
                print(f"benchmark_name: {benchmark_name}\nbenchmark_time: {benchmark_time}\n\n")
                send_result(benchmark_name, benchmark_time)
        if type(results[result]) == pd.DataFrame:
            benchmark_base_name = result
            benchlist = zip(list(results[result].Bookmark), [decode_timecode(x) for x in list(results[result].DrawTime)])
            for subresult in benchlist:
                benchmark_name = f"{benchmark_base_name}_{subresult[0]}_drawtime"
                benchmark_time = subresult[1]
                print(f"benchmark_name: {benchmark_name}\nbenchmark_time: {benchmark_time}\n\n")
                send_result(benchmark_name, benchmark_time)

if upload_zip:
    with zipfile.ZipFile(upload_zip) as z:
        zfiles = {x.filename: z.read(x).decode("utf8") for x in z.filelist}

    results = r17.results(zfiles).results_dict

    display_results = {key: val for key, val in results.items() if type(val) == float and "FPS" not in key}
    c = 0
    drdf = pd.DataFrame(columns=["Benchmark Name", "Benchmark Time"])
    for key, val in display_results.items():
        drdf.loc[c] = (key, val)
        c += 1

    st.dataframe(drdf)

    st.button("Send Results", on_click=send_results)
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json

st.title("View benchmark results")

api_base = "http://localhost:8000/api"

benchmark_list = requests.get(f"{api_base}/get-benchmark-names")
benchmark_list = json.loads(benchmark_list.content)["items"]

display_benchmark = st.selectbox("Select Benchmark", benchmark_list)

benchmark_results = requests.get(f"{api_base}/get-results",
                                 headers={"benchmark": display_benchmark})
jbenchmark_results = json.loads(benchmark_results.content.decode("utf8"))

# st.text(benchmark_results.content.decode("utf8"))

brdf = pd.DataFrame(columns=["time", "computer", "storage"])

c = 0
for jbenchmark in jbenchmark_results["benchmarks"]:
    # st.text(jbenchmark)
    for jbenchmark_result in jbenchmark["benchmark_results"]:
        brdf.loc[c] = (jbenchmark_result, jbenchmark["computer_name"], jbenchmark["storage_name"])
    c += 1

st.dataframe(brdf)

boxchart = px.box(brdf, x="storage", y="time")

st.plotly_chart(boxchart)
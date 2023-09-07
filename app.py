import streamlit as st
from func import *
from llama_cpp import Llama
MODEL_PATH = '/content/ggml-model-q4_1.bin'
n_ctx=2000

data = read_json("/reviews_data_vladimir_pyaterochka.json")
address = st.sidebar.selectbox("Page selection", [address for address in data.keys()])
reviews = get_reviews(data, address)
for r in reviews:
  st.markdown(r)
"""model = Llama(
        model_path=MODEL_PATH,
        n_ctx=n_ctx,
        n_parts=1,
    )

system_tokens = get_system_tokens(model)
tokens = system_tokens
model.eval(tokens)

model_config = {
    "model":model,
    "top_k":30,
    "top_p":0.9,
    "temperature":0.2,
    "repeat_penalty":1.1,
    "tokens":tokens
}
summary = get_summary(reviews, model_config)
st.markdown(summary)"""


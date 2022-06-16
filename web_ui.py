import streamlit as st
import pandas as pd
from cosine_similarity_score import CosineScore
from database import sqlite


def make_clickable(link):
    return f'<a target="_blank" href="{link}">{link}</a>'


# configuration
st.set_page_config(page_title="cosine similarity", layout='wide')
st.header('Cosine Similarity Score')
input_data = st.text_input(label='', placeholder='search somethings')
query = "select link from documents where id = ?"
if input_data:
    cs = CosineScore()
    result = cs.search(input_data)
    result = {sqlite.select(f"select link from documents where id = {k}")[0]['link']: v for k, v in
              sorted(result.items(), key=lambda item: item[1], reverse=True)}
    print(result)
    result = pd.DataFrame(list(result.items()), columns=['link', 'Value'])
    result['link'] = result['link'].apply(make_clickable)
    result = result.to_html(escape=False)
    st.write(result, unsafe_allow_html=True)

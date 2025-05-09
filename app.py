import streamlit as st
import pandas as pd
import random

df = pd.read_csv("quiz.csv")
quiz = df.sample(1).iloc[0]

st.title("日本の地図クイズ")
st.write(quiz["question"])

col1, col2 = st.columns(2)

with col1:
    st.image(f"images/{quiz['image_full']}", caption="地図全体")

with col2:
    st.image(f"images/{quiz['image_zoom']}", caption="拡大図")

choices = quiz["choices"].split(",")
selected = st.radio("選択肢を選んでください", choices)

if st.button("答え合わせ"):
    if selected == quiz["answer"]:
        st.success("正解！")
    else:
        st.error(f"不正解。正解は「{quiz['answer']}」です。")

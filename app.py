import streamlit as st
import pandas as pd
import random
import os

# CSVの読込み
QUIZ_CSV = "quiz.csv"
IMAGE_DIR = "images"

st.set_page_config(page_title="都道府県クイズ", layout="centered")
st.title("\U0001f5fa️ にほんの都道府県クイズ")

# クイズデータの読込み
@st.cache_data
def load_data():
    df = pd.read_csv(QUIZ_CSV)
    return df

df = load_data()

# ランダムに一問出題
quiz = df.sample(1).iloc[0]

# 問題表示
st.subheader(quiz["question"])

col1, col2 = st.columns(2)

with col1:
    st.image(os.path.join(IMAGE_DIR, "full", quiz["image_full"]), caption="全体地図")

with col2:
    st.image(os.path.join(IMAGE_DIR, "zoom", quiz["image_zoom"]), caption="拡大圖")

# 選択肢表示
choices = quiz["choices"].split(",")
random.shuffle(choices)  # 当試の一覧をもう一度シャッフル

selected = st.radio("選んでください:", choices, index=None)

if selected:
    if selected == quiz["answer"]:
        st.success(f"正解です！ 「{selected}」")
    else:
        st.error(f"不正解です！ 正解は 「{quiz['answer']}」")
    
    # 再試行ボタン
    if st.button("別の問題へ"):
        st.experimental_rerun()

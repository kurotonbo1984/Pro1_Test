import streamlit as st
import pandas as pd
import random
import os

# CSVの読み込み
QUIZ_CSV = "quiz.csv"

st.set_page_config(page_title="都道府県クイズ", layout="centered")
st.title("\U0001f5fa️ 日本の都道府県クイズ")

# クイズデータの読み込み
@st.cache_data
def load_data():
    df = pd.read_csv(QUIZ_CSV)
    return df

df = load_data()

# セッションステートの初期化
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected" not in st.session_state:
    st.session_state.selected = None
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = random.randint(0, len(df) - 1)

quiz = df.iloc[st.session_state.quiz_index]

# 問題表示
st.subheader(quiz["question"])

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.image(quiz["image_full"], caption="全体地図", width=450)

with col2:
    st.image(quiz["image_zoom"], caption="拡大図", width=300)

# 選択肢を拡大図の下に表示
st.markdown("### 選択肢")
choices = quiz["choices"].split(",")
random.shuffle(choices)

if not st.session_state.answered:
    selected = st.radio("選んでください:", choices, index=None, key=f"selection_{st.session_state.quiz_index}")
    if selected:
        st.session_state.selected = selected
        st.session_state.answered = True
        st.rerun()
else:
    selected = st.session_state.selected
    col_left, col_right = st.columns([1, 2])
    with col_right:
        if selected == quiz["answer"]:
            st.success(f"✅ 正解です！『{selected}』")
            st.balloons()
        else:
            st.error(f"❌ 不正解です… あなたの答え: 『{selected}』")
            st.markdown(f"### ✅ 正解は『{quiz['answer']}』です！")
            st.snow()

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("🟢 次の問題へ ▶", key="next_button", use_container_width=True):
        st.session_state.quiz_index = random.randint(0, len(df) - 1)
        st.session_state.answered = False
        st.session_state.selected = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

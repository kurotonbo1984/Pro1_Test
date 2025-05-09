import streamlit as st
import pandas as pd
import random
import os

# CSVファイルパス
QUIZ_CSV = "quiz.csv"

st.set_page_config(page_title="都道府県クイズ", layout="centered")
st.title("🗺️ 日本の都道府県クイズ")

# クイズデータを読み込む
@st.cache_data
def load_data():
    return pd.read_csv(QUIZ_CSV)

df = load_data()

# セッションステート初期化
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = random.randint(0, len(df) - 1)
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected" not in st.session_state:
    st.session_state.selected = None

quiz = df.iloc[st.session_state.quiz_index]
choices = quiz["choices"].split(",")
random.shuffle(choices)

st.subheader("この県はどこ？")

# --- 回答前 ---
if not st.session_state.answered:
    col1, col2 = st.columns([1.5, 1], gap="large")
    with col1:
        st.image(os.path.join("images", "full", quiz["image_full"]), caption="全体地図", width=450)
    with col2:
        st.image(os.path.join("images", "zoom", quiz["image_zoom"]), caption="拡大図", width=300)

    st.markdown("### 選択肢")
    selected = st.radio("選んでください:", choices, index=None)

    if selected:
        st.session_state.selected = selected
        st.session_state.answered = True

# --- 回答後 ---
else:
    selected = st.session_state.selected
    correct = selected == quiz["answer"]

    st.markdown("---")
    if correct:
        st.markdown(f"<h1 style='text-align: center; color: green;'>✅ 正解！『{selected}』</h1>", unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f"<h1 style='text-align: center; color: red;'>❌ 不正解… 『{selected}』</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: green;'>正解は 『{quiz['answer']}』 です</h2>", unsafe_allow_html=True)
        st.snow()

    # 「次の問題へ」ボタン
    st.markdown("---")
    if st.button("🟢 次の問題へ ▶", use_container_width=True):
        st.session_state.quiz_index = random.randint(0, len(df) - 1)
        st.session_state.answered = False
        st.session_state.selected = None
        st.rerun()

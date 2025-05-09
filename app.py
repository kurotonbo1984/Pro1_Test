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
if "total" not in st.session_state:
    st.session_state.total = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0

quiz = df.iloc[st.session_state.quiz_index]

# 問題表示
st.subheader(quiz["question"])

# 選択肢をランダムに
choices = quiz["choices"].split(",")
random.shuffle(choices)

# 画像と選択肢表示 or フィードバックのみ表示
if not st.session_state.answered:
    # 地図画像の表示（現在のファイルと同じディレクトリから読み込む）
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.image(os.path.join(os.path.dirname(__file__), quiz["image_full"]), caption="全体地図", width=450)
    with col2:
        st.image(os.path.join(os.path.dirname(__file__), quiz["image_zoom"]), caption="拡大図", width=300)

    st.markdown("### 選択肢")
    cols = st.columns(2)
    for i, choice in enumerate(choices):
        if cols[i % 2].button(choice, key=f"choice_{i}_{st.session_state.quiz_index}"):
            st.session_state.selected = choice
            st.session_state.answered = True
            st.session_state.total += 1
            if choice == quiz["answer"]:
                st.session_state.correct += 1
            st.rerun()
else:
    selected = st.session_state.selected
    correct = selected == quiz["answer"]

    # 地図を非表示にしてフィードバックのみ表示
    st.markdown("---")
    if correct:
        st.markdown(f"<h1 style='text-align: center; color: green; font-size: 48px;'>✅ 正解！『{selected}』</h1>", unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f"<h1 style='text-align: center; color: red; font-size: 48px;'>❌ 不正解… 『{selected}』</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: green; font-size: 36px;'>正解は『{quiz['answer']}』です</h2>", unsafe_allow_html=True)
        st.snow()

    # スコア表示
    st.markdown(f"<p style='text-align: center; font-size: 20px;'>正解数: {st.session_state.correct} / {st.session_state.total}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("🟢 次の問題へ ▶", key=f"next_button_{st.session_state.total}", use_container_width=True):
        st.session_state.quiz_index = random.randint(0, len(df) - 1)
        st.session_state.answered = False
        st.session_state.selected = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

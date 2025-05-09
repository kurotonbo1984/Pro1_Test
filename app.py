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

# 選択肢をランダムに（ただし quiz_index ごとに一貫性を持たせる）
if "shuffled_choices" not in st.session_state or st.session_state.get("last_quiz_index") != st.session_state.quiz_index:
    st.session_state.shuffled_choices = quiz["choices"].split(",")
    random.shuffle(st.session_state.shuffled_choices)
    st.session_state.last_quiz_index = st.session_state.quiz_index
choices = st.session_state.shuffled_choices

# 回答前の処理
if not st.session_state.answered:
    # 地図画像の表示（現在のファイルと同じディレクトリから読み込む）
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.image(os.path.join(os.path.dirname(__file__), quiz["image_full"]), caption="全体地図", width=600)
    with col2:
        st.image(os.path.join(os.path.dirname(__file__), quiz["image_zoom"]), caption="拡大図", width=250)

    st.markdown("### 選択肢")
    cols = st.columns(2)
    for i, choice in enumerate(choices):
        if cols[i % 2].button(choice, key=f"choice_{i}_{st.session_state.quiz_index}_{st.session_state.total}"):
            st.session_state.selected = choice
            st.rerun()

    if st.session_state.selected:
        st.markdown(f"選択中: 『{st.session_state.selected}』")

    if st.button("✅ 回答する", key="submit_answer"):
        st.session_state.answered = True
        st.session_state.total += 1
        if st.session_state.selected == quiz["answer"]:
            st.session_state.correct += 1
        st.rerun()

# 回答後の処理
else:
    selected = st.session_state.selected if st.session_state.selected else "無回答"
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

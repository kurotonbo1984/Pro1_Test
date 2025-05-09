import streamlit as st
import pandas as pd
import zipfile
import os

# 初期実行：prefectures.zip を展開
if not os.path.exists("prefectures.geojson") and os.path.exists("prefectures.zip"):
    with zipfile.ZipFile("prefectures.zip", 'r') as zip_ref:
        zip_ref.extractall(".")

# クイズデータを読み込み
quiz_df = pd.read_csv("quiz.csv", encoding="utf-8")

# 現在の問題番号（セッション状態で管理）
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# 現在の問題を取得
q = quiz_df.iloc[st.session_state.question_index]

st.title("🗾 都道府県クイズ")

st.subheader(f"Q{q['id']}：{q['question']}")

# 画像の表示（全体図＋拡大図）
col1, col2 = st.columns(2)
with col1:
    st.image(f"images/full/{q['image_full']}", caption="全体図", use_column_width=True)
with col2:
    st.image(f"images/zoom/{q['image_zoom']}", caption="拡大図", use_column_width=True)

# 選択肢を表示
choices = q['choices'].split(",")
answer = q['answer']
user_choice = st.radio("この都道府県は？", choices)

# 回答ボタン
if st.button("回答する"):
    if user_choice == answer:
        st.success("✅ 正解です！")
        st.session_state.score += 1
    else:
        st.error(f"❌ 不正解。正解は {answer} でした。")

    # 次の問題へ
    if st.session_state.question_index + 1 < len(quiz_df):
        st.session_state.question_index += 1
        st.experimental_rerun()
    else:
        st.balloons()
        st.markdown(f"### 🎉 クイズ終了！あなたのスコアは {st.session_state.score} / {len(quiz_df)}")
        if st.button("最初からやり直す"):
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.experimental_rerun()

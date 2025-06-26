# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 13:00:39 2025

@author: Christine
"""

import streamlit as st
import pandas as pd
import random

# 初始化狀態
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_data = []
    st.session_state.show_result = False

# 讀取單字表
df = pd.read_excel("en_cn_vn.xlsx")
df.columns = df.columns.str.lower()
df = df.dropna()

LANGUAGES = {
    "English": "english",
    "中文": "chinese",
    "Tiếng Việt": "vietnamese"
}

st.title("🌏 多語單字練習系統")

# 選擇目標語言
target_lang_label = st.selectbox("你想要練習哪個語言？", list(LANGUAGES.keys()))
target_lang = LANGUAGES[target_lang_label]
question_langs = [l for l in LANGUAGES.values() if l != target_lang]

# 開始測驗按鈕
if st.button("🎯 開始新測驗"):
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.show_result = False
    st.session_state.quiz_data = random.sample(list(df.itertuples(index=False)), 3)

# 若測驗已啟動
if st.session_state.quiz_data and not st.session_state.show_result:
    q = st.session_state.quiz_data[st.session_state.current_question]._asdict()
    
    st.markdown(f"### 第 {st.session_state.current_question + 1} 題")
    st.write(f"👉 {question_langs[0].capitalize()}: `{q[question_langs[0]]}`")
    st.write(f"👉 {question_langs[1].capitalize()}: `{q[question_langs[1]]}`")
    
    answer = st.text_input("請輸入你的答案", key=f"answer_{st.session_state.current_question}")
    
    if st.button("提交答案", key=f"submit_{st.session_state.current_question}"):
        correct_answer = str(q[target_lang]).strip().lower()
        if answer.strip().lower() == correct_answer:
            st.success("✅ 正確！")
            st.session_state.score += 1
        else:
            st.error(f"❌ 錯誤，正確答案是：{q[target_lang]}")
        
        st.session_state.current_question += 1
        
        if st.session_state.current_question >= 3:
            st.session_state.show_result = True

# 顯示測驗結果
if st.session_state.show_result:
    st.markdown("---")
    st.markdown(f"## 🎉 測驗完成！你總共答對 `{st.session_state.score}` / 3 題")
    if st.button("🔁 再玩一次"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.show_result = False
        st.session_state.quiz_data = random.sample(list(df.itertuples(index=False)), 3)

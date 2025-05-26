import streamlit as st
import sqlite3
import pandas as pd

# SQLite DB 파일 경로
DB_PATH = "illey.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            job TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_entries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, job FROM entries ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_entry(name, job):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO entries (name, job) VALUES (?, ?)", (name, job))
    conn.commit()
    cur.close()
    conn.close()

init_db()

st.title("간단 정보 수집")

# 기존 접수 내역 표시
rows = get_entries()
if rows:
    st.subheader("현재까지 접수된 내역")
    df = pd.DataFrame(rows, columns=["업체명", "업종"])
    st.table(df)
else:
    st.info("아직 접수된 내역이 없습니다.")

name = st.text_input("업체명(혹은 이름)")
job = st.text_input("업종(혹은 무슨일)")

if st.button("제출"):
    if name and job:
        add_entry(name, job)
        st.success("제출이 완료되었습니다!")
        st.experimental_rerun()
    else:
        st.warning("모든 항목을 입력해주세요.")
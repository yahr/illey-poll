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
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("PRAGMA table_info(entries)")
    columns = [row[1] for row in cur.fetchall()]
    if 'phone' not in columns:
        cur.execute("ALTER TABLE entries ADD COLUMN phone TEXT")
    conn.commit()
    cur.close()
    conn.close()

def get_entries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, job, phone FROM entries ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_entry(name, job, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO entries (name, job, phone) VALUES (?, ?, ?)", (name, job, phone))
    conn.commit()
    cur.close()
    conn.close()

def delete_entry(entry_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()
    cur.close()
    conn.close()

init_db()

st.title("제일광고기획 거래처 관리")

# 기존 접수 내역 표시
rows = get_entries()
if rows:
    st.subheader("현재까지 접수된 내역")
    # 표 헤더
    col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
    col1.markdown("**업체명**")
    col2.markdown("**업종**")
    col3.markdown("**연락처**")
    col4.markdown("**삭제**")
    # 데이터 행
    for row in rows:
        id_, name, job, phone = row
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
        col1.write(name)
        col2.write(job)
        col3.write(phone if phone else "-")
        if col4.button("삭제", key=f"delete_{id_}"):
            delete_entry(id_)
            st.success(f"{name} 데이터가 삭제되었습니다.")
            st.rerun()
else:
    st.info("아직 접수된 내역이 없습니다.")

name = st.text_input("업체명(혹은 이름)")
job = st.text_input("업종(혹은 무슨일)")
phone = st.text_input("연락처")

if st.button("제출"):
    if name and job:
        add_entry(name, job, phone)
        st.success("제출이 완료되었습니다!")
        st.rerun()
    else:
        st.warning("업체명과 업종을 모두 입력해주세요.")
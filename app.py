import streamlit as st
import re
import pandas as pd
from datetime import datetime

# Настройка: Чистый и мощный терминал
st.set_page_config(page_title="АВТО-УЗЕЛ", layout="wide")

# Единая библиотека встреч (База данных)
if 'hub_db' not in st.session_state:
    st.session_state.hub_db = []

st.title("🎯 АВТО-ХАНТЕР: МЕСТО ВСТРЕЧИ")
st.write("Соединяем тех, кто ищет, с теми, у кого есть. Без посредников в товаре.")

# --- БЛОК 1: КТО ИЩЕТ (СПРОС) ---
with st.expander("🔍 Я ИЩУ ЗАПЧАСТЬ (ЗАЯВКА)"):
    c1, c2 = st.columns(2)
    with c1:
        part_needed = st.text_input("Марка и Деталь:", placeholder="Например: BMW E60 Бампер")
    with c2:
        buyer_tel = st.text_input("Ваш контакт:", placeholder="+375...")
    
    if st.button("📢 ОПУБЛИКОВАТЬ ЗАПРОС"):
        if part_needed and buyer_tel:
            st.session_state.hub_db.append({
                "Дата": datetime.now().strftime("%H:%M"),
                "Статус": "ИЩУТ", "Объект": part_needed.upper(), "Контакт": buyer_tel
            })
            st.success("Запрос в эфире!")

st.divider()

# --- БЛОК 2: КТО ПРОДАЕТ (ПРЕДЛОЖЕНИЕ - ИЗ ЧАТОВ И НАПРЯМУЮ) ---
with st.expander("🚚 У МЕНЯ ЕСТЬ ЗАПЧАСТИ (ПРЕДЛОЖЕНИЕ / ЧАТЫ)"):
    raw_input = st.text_area("Вставьте текст из чата или ваше предложение:", height=150)
    if st.button("🚀 ДОБАВИТЬ В ЭФИР"):
        # Вытаскиваем номера телефонов
        found_tels = list(set(re.findall(r'(?:\+|\b)(?:\d[\s\-]?){10,14}\d', raw_input)))
        if found_tels:
            for t in found_tels:
                st.session_state.hub_db.append({
                    "Дата": datetime.now().strftime("%H:%M"),
                    "Статус": "ПРОДАЮТ", "Объект": "Запчасти (см. контакт)", "Контакт": t
                })
            st.success(f"Добавлено {len(found_tels)} предложений!")
        else:
            st.warning("Контакты не найдены.")

st.divider()

# --- БЛОК 3: БИБЛИОТЕКА ВСТРЕЧ (ТВОЙ РЫНОК) ---
st.subheader("📚 ЖИВОЙ ЭФИР РЫНКА")

if st.session_state.hub_db:
    df = pd.DataFrame(st.session_state.hub_db).drop_duplicates(subset=['Контакт', 'Объект'])
    
    # ФИЛЬТР ДЛЯ СТЫКОВКИ
    search_match = st.text_input("🔍 НАЙТИ ПАРУ (введите название детали):")
    if search_match:
        df = df[df['Объект'].str.contains(search_match, case=False)]

    st.table(df.tail(20)) # Твоя витрина встреч
    
    # Кнопка СКАЧАТЬ ВЕСЬ ЭФИР (Excel)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 СКАЧАТЬ БАЗУ ДЛЯ ОБЗВОНА (EXCEL)", csv, "auto_hub.csv", "text/csv")
    
    st.divider()
    # БЫСТРЫЙ ВЫЗОВ (Клик — и они встретились!)
    st.subheader("📲 СВЯЗАТЬ УЧАСТНИКОВ:")
    for index, row in df.tail(5).iterrows():
        clean_p = re.sub(r'[^\d+]', '', row['Контакт'])
        btn_label = f"📞 {row['Статус']}: {row['Объект']} — {row['Контакт']}"
        st.link_button(btn_label, f"tel:{clean_p}", use_container_width=True)
else:
    st.info("В эфире пока тишина. Начните наполнение!")

st.caption("Платформа: ARV-04 | Место встречи продавцов и покупателей")

import streamlit as st
import re
import pandas as pd
from datetime import datetime

# 1. Настройка: Широкий экран и русский заголовок
st.set_page_config(page_title="Авто-Хантер: Помощник", layout="wide")

# Инициализация Библиотеки (памяти)
if 'db' not in st.session_state:
    st.session_state.db = []

st.title("🎯 ВАШ АВТО-ПОМОЩНИК")

# 2. БЛОК УПРАВЛЕНИЯ (ДЛЯ ГЕНЕРАЛЬНОГО)
with st.expander("⚙️ НАСТРОЙКА СЛЕЖКИ И УВЕДОМЛЕНИЙ"):
    enable_alert = st.checkbox("🔔 ВКЛЮЧИТЬ ОПОВЕЩЕНИЕ ПРИ НАХОДКЕ", value=False)
    watch_word = st.text_input("Какую деталь или марку ловим?", value="КПП")

# 3. ПОЛЕ ДЛЯ НОВЫХ ПОСТУПЛЕНИЙ (СЮДА КИДАЕМ ТЕКСТ)
raw_input = st.text_area("📥 ВСТАВЬТЕ ТЕКСТ ИЗ ЧАТОВ (VIBER, TG, САЙТЫ):", height=150)

if st.button("🚀 ОБРАБОТАТЬ И ВНЕСТИ В БАЗУ"):
    if raw_input:
        # Ищем телефоны
        new_phones = list(set(re.findall(r'(?:\+|\b)(?:\d[\s\-]?){10,14}\d', raw_input)))
        
        if new_phones:
            # Сработка уведомления
            if enable_alert and watch_word.lower() in raw_input.lower():
                st.error(f"🚨 ЕСТЬ ЗАКАЗ! Найдена деталь: {watch_word}")
                st.balloons()
            
            # Наполняем Библиотеку
            for p in new_phones:
                st.session_state.db.append({
                    "Время": datetime.now().strftime("%H:%M"),
                    "Контакт": p,
                    "Деталь": watch_word if enable_alert else "Общий поиск"
                })
            st.success(f"Добавлено {len(new_phones)} новых контактов в базу!")
    else:
        st.error("Поле пустое!")

st.divider()

# 4. ТВОЯ БИБЛИОТЕКА (ТОТ САМЫЙ СКЛАД)
st.subheader("📚 ВАША БИБЛИОТЕКА ЗАПЧАСТЕЙ")

if st.session_state.db:
    df = pd.DataFrame(st.session_state.db).drop_duplicates(subset=['Контакт'])
    
    # Поиск по библиотеке (чтобы вытащить то, что нужно)
    search_q = st.text_input("🔍 Поиск по накопленной базе (введите номер или деталь):")
    if search_q:
        df = df[df['Контакт'].str.contains(search_q) | df['Деталь'].str.contains(search_q, case=False)]

    st.table(df.tail(10)) # Показываем последние 10 записей
    
    # Кнопка СКАЧАТЬ (Монетизация)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 СКАЧАТЬ ВЕСЬ СКЛАД (EXCEL)", csv, "auto_base.csv", "text/csv")

    st.divider()
    # Кнопки для быстрого обзвона из последних находок
    for index, row in df.tail(5).iterrows():
        clean_p = re.sub(r'[^\d+]', '', row['Контакт'])
        st.link_button(f"📞 ПОЗВОНИТЬ {row['Контакт']} ({row['Деталь']})", f"tel:{clean_p}", use_container_width=True)
else:
    st.info("Библиотека пока пуста. Закиньте первый текст выше.")

st.caption("Бизнес-платформа: ARV-04 | Система активна")

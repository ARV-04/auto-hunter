import streamlit as st
import re

# Настройка страницы "под телефон"
st.set_page_config(page_title="Auto Hunter AI", page_icon="🚗")

# --- 1. ЗАЩИТА (ТВОЙ ПАРОЛЬ) ---
password = st.sidebar.text_input("Введи ключ доступа:", type="password")
if password != "MINSK2026":
    st.warning("🔒 Введите пароль в боковой панели, чтобы разблокировать утилиту.")
    st.stop()

st.title("🚗 Auto Hunter: Перехват")
st.write("Вставь текст — я найду контакты и сделаю их кликабельными.")

# --- 2. ВВОД ДАННЫХ ---
raw_text = st.text_area("👇 Вставь данные (Kufar / чаты / сайты):", height=250)

if st.button("🚀 НАЙТИ ТЕЛЕФОНЫ И ССЫЛКИ"):
    if raw_text:
        # Регулярки: ищем ссылки, почты и БЕЛОРУССКИЕ ТЕЛЕФОНЫ
        emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)))
        urls = list(set(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw_text)))
        phones = list(set(re.findall(r'\+?375\s?\(?\d{2}\)?\s?\d{3}-?\d{2}-?\d{2}', raw_text)))

        st.divider()

        # --- 3. ВЫВОД РЕЗУЛЬТАТОВ (ТВОЯ ФИЧА "ПОЗВОНИТЬ") ---
        if phones:
            st.subheader(f"📞 Найдено телефонов: {len(phones)}")
            for p in phones:
                # Очищаем номер от лишних знаков для звонка
                clean_phone = re.sub(r'[^0-9+]', '', p)
                # Кнопка, которая открывает "дозвон" в телефоне
                st.link_button(f"📞 ПОЗВОНИТЬ {p}", f"tel:{clean_phone}")
        
        if urls:
            st.subheader(f"🔗 Ссылки: {len(urls)}")
            for u in urls:
                st.write(u)
                
        if not phones and not urls:
            st.info("Ничего ценного не найдено. Попробуй другой текст.")
    else:
        st.error("Поле пустое!")

st.sidebar.markdown("---")
st.sidebar.caption("v1.2 | Автор: ARV-04")import streamlit as st
import re

# Настройка страницы "под телефон"
st.set_page_config(page_title="Auto Hunter AI", page_icon="🚗")

# --- 1. ЗАЩИТА (ТВОЙ ПАРОЛЬ) ---
password = st.sidebar.text_input("Введи ключ доступа:", type="password")
if password != "MINSK2026":
    st.warning("🔒 Введите пароль в боковой панели, чтобы разблокировать утилиту.")
    st.stop()

st.title("🚗 Auto Hunter: Перехват")
st.write("Вставь текст — я найду контакты и сделаю их кликабельными.")

# --- 2. ВВОД ДАННЫХ ---
raw_text = st.text_area("👇 Вставь данные (Kufar / чаты / сайты):", height=250)

if st.button("🚀 НАЙТИ ТЕЛЕФОНЫ И ССЫЛКИ"):
    if raw_text:
        # Регулярки: ищем ссылки, почты и БЕЛОРУССКИЕ ТЕЛЕФОНЫ
        emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)))
        urls = list(set(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw_text)))
        phones = list(set(re.findall(r'\+?375\s?\(?\d{2}\)?\s?\d{3}-?\d{2}-?\d{2}', raw_text)))

        st.divider()

        # --- 3. ВЫВОД РЕЗУЛЬТАТОВ (ТВОЯ ФИЧА "ПОЗВОНИТЬ") ---
        if phones:
            st.subheader(f"📞 Найдено телефонов: {len(phones)}")
            for p in phones:
                # Очищаем номер от лишних знаков для звонка
                clean_phone = re.sub(r'[^0-9+]', '', p)
                # Кнопка, которая открывает "дозвон" в телефоне
                st.link_button(f"📞 ПОЗВОНИТЬ {p}", f"tel:{clean_phone}")
        
        if urls:
            st.subheader(f"🔗 Ссылки: {len(urls)}")
            for u in urls:
                st.write(u)
                
        if not phones and not urls:
            st.info("Ничего ценного не найдено. Попробуй другой текст.")
    else:
        st.error("Поле пустое!")

st.sidebar.markdown("---")
st.sidebar.caption("v1.2 | Автор: ARV-04")

import streamlit as st
import re
import pandas as pd

# 1. Настройка: Чистый экран, ничего лишнего
st.set_page_config(page_title="Хантер: Сервис", layout="wide")

# Скрываем технический мусор Streamlit (меню, футеры)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3.5em; 
        background-color: #ff4b4b; color: white; font-weight: bold; font-size: 20px;
    }
    </style>
    """, unsafe_allow_code=True)

# Функция звука (сигнал клиенту)
def play_alert():
    st.markdown('<audio autoplay><source src="https://www.soundjay.com"></audio>', unsafe_allow_code=True)

st.title("🎯 ХАНТЕР: ПУЛЬТ УПРАВЛЕНИЯ")

# БЛОК ДЛЯ КЛИЕНТА (ВСЕГО ДВЕ НАСТРОЙКИ)
col_cfg1, col_cfg2 = st.columns(2)
with col_cfg1:
    enable_hunt = st.checkbox("🔔 ВКЛЮЧИТЬ СЛЕЖКУ ЗА ДЕТАЛЬЮ", value=False)
with col_cfg2:
    target_part = st.text_input("ЧТО ИЩЕМ?", value="КПП", label_visibility="collapsed")

st.divider()

# ГЛАВНОЕ ОКНО
raw_text = st.text_area("ВСТАВЬТЕ ТЕКСТ ИЗ ЧАТОВ СЮДА:", height=250, placeholder="Скопируйте сюда переписку из Viber или Telegram...")

if st.button("🚀 НАЧАТЬ ПОИСК"):
    if raw_text:
        # Поиск номеров
        phones = list(set(re.findall(r'(?:\+|\b)(?:\d[\s\-]?){10,14}\d', raw_text)))
        
        if phones:
            # СРАБОТКА (ЕСЛИ ВКЛЮЧЕНА СЛЕЖКА)
            if enable_hunt and target_part.lower() in raw_text.lower():
                st.error(f"🚨 ЕСТЬ СОВПАДЕНИЕ! НАЙДЕНА ДЕТАЛЬ: {target_part}")
                play_alert()
                st.balloons()

            st.subheader(f"✅ Найдено контактов: {len(phones)}")
            
            # ВЫВОД КНОПОК ПОД ПАЛЕЦ
            for p in phones:
                clean_p = re.sub(r'[^\d+]', '', p)
                if not clean_p.startswith('+') and len(clean_p) > 10:
                    clean_p = '+' + clean_p
                # Огромная кнопка вызова
                st.link_button(f"📞 ПОЗВОНИТЬ {p}", f"tel:{clean_p}")
        else:
            st.warning("В этом тексте номеров не найдено.")
    else:
        st.error("Поле пустое! Вставьте данные для поиска.")

st.caption("Лицензионный доступ: ARV-04 | Сервис активен")

import streamlit as st
import re
import pandas as pd

# 1. Настройка: Только самое важное
st.set_page_config(page_title="Хантер", layout="wide")

st.title("🎯 ХАНТЕР: ПУЛЬТ УПРАВЛЕНИЯ")

# 2. ДВЕ КНОПКИ ДЛЯ КЛИЕНТА (СЛЕЖКА)
col_cfg1, col_cfg2 = st.columns(2)
with col_cfg1:
    enable_hunt = st.checkbox("🔔 ВКЛЮЧИТЬ СЛЕЖКУ ЗА ДЕТАЛЬЮ", value=False)
with col_cfg2:
    target_part = st.text_input("ЧТО ИЩЕМ?", value="КПП", label_visibility="collapsed")

st.divider()

# 3. ГЛАВНОЕ ОКНО ДЛЯ ТЕКСТА
raw_text = st.text_area("ВСТАВЬТЕ ТЕКСТ ИЗ ЧАТОВ СЮДА:", height=250, placeholder="Скопируйте переписку...")

if st.button("🚀 НАЧАТЬ ПОИСК"):
    if raw_text:
        # Ищем номера
        phones = list(set(re.findall(r'(?:\+|\b)(?:\d[\s\-]?){10,14}\d', raw_text)))
        
        if phones:
            # СРАБОТКА УВЕДОМЛЕНИЯ
            if enable_hunt and target_part.lower() in raw_text.lower():
                st.error(f"🚨 ЕСТЬ СОВПАДЕНИЕ! НАЙДЕНА ДЕТАЛЬ: {target_part}")
                # Звуковой сигнал
                st.markdown('<audio autoplay><source src="https://www.soundjay.com"></audio>', unsafe_allow_code=True)
                st.balloons()

            st.subheader(f"✅ Найдено контактов: {len(phones)}")
            
            # ВЫВОД КНОПОК ПОД ПАЛЕЦ
            for p in phones:
                clean_p = re.sub(r'[^\d+]', '', p)
                if not clean_p.startswith('+') and len(clean_p) > 10:
                    clean_p = '+' + clean_p
                # Жирная кнопка вызова
                st.link_button(f"📞 ПОЗВОНИТЬ {p}", f"tel:{clean_p}", use_container_width=True)
        else:
            st.warning("Номера не найдены.")
    else:
        st.error("Поле пустое!")

st.caption("Лицензионный доступ: ARV-04 | Сервис активен")

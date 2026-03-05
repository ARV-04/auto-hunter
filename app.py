import streamlit as st
import re
import pandas as pd

# Настройка Агрегатора (Широкий экран)
st.set_page_config(page_title="Хантер: База", layout="wide")

st.title("🎯 АВТО-ХАНТЕР: БАЗА И ЗВОНКИ")

# Блок настройки уведомлений (твое пожелание)
with st.expander("🔔 НАСТРОЙКА УВЕДОМЛЕНИЙ (ОБНОВЛЕНИЕ)"):
    target_part = st.text_input("Какую запчасть отслеживаем?", placeholder="Например: КПП или Бампер")
    st.info("Система подсветит запросы, если найдет это слово в тексте.")

# Поле для сырого текста
raw_text = st.text_area("ВСТАВЬ ТЕКСТ ИЗ ЧАТОВ СЮДА:", height=200)

if st.button("🚀 ОБРАБОТАТЬ И ВНЕСТИ В БАЗУ"):
    if raw_text:
        # Ищем телефоны (РФ, РБ, СНГ)
        phones = list(set(re.findall(r'(?:\+|\b)(?:\d[\s\-]?){10,14}\d', raw_text)))
        
        if phones:
            st.success(f"✅ Найдено контактов: {len(phones)}")
            
            # Если есть ключевое слово — проверяем его
            if target_part and target_part.lower() in raw_text.lower():
                st.warning(f"🎯 ВНИМАНИЕ! Найдено совпадение по запчасти: {target_part}")

            # Создаем таблицу (Библиотеку)
            df = pd.DataFrame(phones, columns=["Контакт"])
            st.table(df) # Визуальная таблица
            
            # Кнопка СКАЧАТЬ В EXCEL (твоя монетизация)
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 СКАЧАТЬ ВСЮ БАЗУ (EXCEL)", csv, "auto_base.csv", "text/csv")
            
            st.divider()
            
            # ГЛАВНОЕ: Кнопки для моментального звонка
            st.subheader("📲 БЫСТРЫЙ ОБЗВОН (БЕЗ ВВОДА НОМЕРА):")
            for p in phones:
                # Чистим номер для системы звонка
                clean_p = re.sub(r'[^\d+]', '', p)
                if not clean_p.startswith('+') and len(clean_p) > 10:
                    clean_p = '+' + clean_p
                
                # Кнопка звонка (нажал — позвонил)
                st.link_button(f"📞 ПОЗВОНИТЬ: {p}", f"tel:{clean_p}", use_container_width=True)
        else:
            st.warning("В этом тексте номеров не найдено.")
    else:
        st.error("Пусто! Закинь данные из Viber/Telegram.")

st.caption("Система: ARV-04 | Генеральный директор | Звонки активны")

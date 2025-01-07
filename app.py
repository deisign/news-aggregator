import streamlit as st
import feedparser
from datetime import datetime

# --- Функция для получения новостей из RSS ---
def fetch_rss_news(rss_feeds):
    news_list = []
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        if feed.entries:  # Проверяем, есть ли данные в ленте
            st.sidebar.info(f"✅ {feed_url} - Найдено новостей: {len(feed.entries)}")
            for entry in feed.entries:
                news_list.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published if 'published' in entry else "Не указано",
                    "source": feed_url
                })
        else:
            st.sidebar.warning(f"⚠️ {feed_url} - Нет данных")
    return news_list

# --- Списки источников ---
rss_feeds = [
    # Калмыкия
    
    'https://kalmykia-news.net/rss/news',
    'https://vesti-kalmykia.ru/feed/rss/news?format=feed',
    'http://halmgynn.ru/rss.xml',  # Новый источник
    # Ингушетия
    'https://fortanga.org/feed',
    'https://magastimes.ru/feed',
]

telegram_channels = [
    # Калмыкия
    'https://t.me/kalmyk_broadcast',
    'https://t.me/riakalm',
    'https://t.me/kalmykiya_news',
    'https://t.me/elistacity',
    'https://t.me/boombakalmykia',
    'https://t.me/vesti_kalmykia',
    'https://t.me/insider_kalmykia',
    'https://t.me/kalmykia_online',
    'https://t.me/slukhach_kalmykia',
    'https://t.me/elistapano',
    # Ингушетия
    'https://t.me/ingushetia_official',
    'https://t.me/ingushetiya_daily',
    'https://t.me/ingushsegodnya',
    'https://t.me/ingushetiatg',
]

# --- Заголовок приложения ---
st.title("Агрегатор новостей Калмыкии и Ингушетии")
st.sidebar.header("Фильтры")

# --- Получение и отображение новостей из RSS ---
st.sidebar.subheader("Статус лент:")
news = fetch_rss_news(rss_feeds)

# Фильтрация по источнику
sources = list(set([n['source'] for n in news]))
selected_sources = st.sidebar.multiselect(
    "Выберите источники (RSS)", options=sources, default=sources
)

# Фильтрация по ключевым словам
keywords = st.sidebar.text_input("Фильтр по ключевым словам", "")

# Применение фильтров
filtered_news = [
    n for n in news
    if n['source'] in selected_sources and (keywords.lower() in n['title'].lower() or keywords == "")
]

# --- Вывод новостей из RSS ---
st.subheader(f"Найдено новостей (RSS): {len(filtered_news)}")
for item in filtered_news:
    st.markdown(f"### [{item['title']}]({item['link']})")
    st.markdown(f"*Источник:* {item['source']}")
    st.markdown(f"*Дата публикации:* {item['published']}")
    st.write("---")

# --- Вывод Telegram-каналов ---
st.subheader("Telegram-каналы")
st.write("Ниже представлены ссылки на Telegram-каналы Калмыкии и Ингушетии. Для просмотра содержимого перейдите по ссылке:")
for channel in telegram_channels:
    st.markdown(f"- [Перейти в Telegram]({channel})")

# --- Информация о приложении ---
st.sidebar.info(
    """
    Это приложение создано для агрегирования новостей из регионов Калмыкия и Ингушетия.
    Источники: RSS-ленты и Telegram-каналы.
    """
)

import streamlit as st
import feedparser
from telethon.sync import TelegramClient

# --- Конфигурация Telegram API ---
api_id = 20273444
api_hash = 'a8585366cd62cd366d52ba03bc366508'

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

# --- Функция для получения данных из Telegram-каналов ---
def fetch_telegram_messages(client, channels):
    messages = []
    for channel in channels:
        try:
            entity = client.get_entity(channel)
            for message in client.iter_messages(entity, limit=10):  # Получаем последние 10 сообщений
                if message.message:
                    messages.append({
                        "channel": channel,
                        "text": message.message.strip(),
                        "date": message.date
                    })
        except Exception as e:
            st.sidebar.error(f"Ошибка при обработке {channel}: {e}")
    return messages

# --- Списки источников ---
rss_feeds = [
    # Калмыкия
    'https://kalmykia-news.net/rss/news',
    'https://elista.bezformata.com/rsstop.xml',
    'https://vesti-kalmykia.ru/feed/rss/news?format=feed',
    'http://halmgynn.ru/rss.xml',
    # Ингушетия
    'https://fortanga.org/feed',
    'https://magastimes.ru/feed',
]

telegram_channels = [
    'https://t.me/kalmnovosti',
    'https://t.me/elistaorg',
    'https://t.me/s/riakalm',
    'https://t.me/s/kalmykiya_news',
    'https://t.me/gorodelista1',
    'https://t.me/governmentkalmykia08',
    'https://t.me/OkElista',
    'https://t.me/kalmykia08',
    'https://t.me/Fond_ZO_Kalmykia',
    'https://t.me/cphelista',
    'https://t.me/adm_ket',
    'https://t.me/infokalmykiya',
    'https://t.me/molodezhy08',
    'https://t.me/kalmstat',
    'https://t.me/PozornayaDoskaElista',
    'https://t.me/sluhi_08',
    'https://t.me/insider08',
    'https://t.me/mcrrk',
    'https://t.me/mypervie08',
    'https://t.me/KhurulKalmykia',
    'https://t.me/elstvibe',
    'https://t.me/elistaonline',
    'https://t.me/kalmykia_08_rk',
    'https://t.me/vesti_kalmykia',
    'https://t.me/bumba_bumba',
    'https://t.me/Kalmgame08',
    'https://t.me/s/ingushetiya_daily',
    'https://t.me/golos_ingushetii',
    'https://t.me/RIA_Ingushetia',
    'https://t.me/su_skr06',
    'https://t.me/vesti_ingush',
    'https://t.me/ingushetia_official',
    'https://t.me/d5U0OXuvYt8zM2Q6',
    'https://t.me/vecheringushetiya',
    'https://t.me/gazetaingush',
    'https://t.me/segondya06',
    'https://t.me/rozyskRI',
    'https://t.me/ingsobranie',
    'https://t.me/s/themagastimes',
    'https://t.me/s/fortangaorg'
]

# --- Заголовок приложения ---
st.title("Агрегатор новостей Калмыкии и Ингушетии")
st.sidebar.header("Фильтры")

# --- Получение новостей из RSS ---
st.sidebar.subheader("Статус лент:")
rss_news = fetch_rss_news(rss_feeds)

# --- Получение новостей из Telegram ---
with TelegramClient('session_name', api_id, api_hash) as client:
    st.sidebar.subheader("Telegram-каналы")
    telegram_news = fetch_telegram_messages(client, telegram_channels)

# --- Фильтрация по источникам и ключевым словам ---
sources = list(set([n['source'] for n in rss_news]))
selected_sources = st.sidebar.multiselect(
    "Выберите источники (RSS)", options=sources, default=sources
)
keywords = st.sidebar.text_input("Фильтр по ключевым словам", "")

filtered_rss_news = [
    n for n in rss_news
    if n['source'] in selected_sources and (keywords.lower() in n['title'].lower() or keywords == "")
]

filtered_telegram_news = [
    n for n in telegram_news
    if keywords.lower() in n['text'].lower() or keywords == ""
]

# --- Вывод новостей из RSS ---
st.subheader(f"Найдено новостей (RSS): {len(filtered_rss_news)}")
for item in filtered_rss_news:
    st.markdown(f"### [{item['title']}]({item['link']})")
    st.markdown(f"*Источник:* {item['source']}")
    st.markdown(f"*Дата публикации:* {item['published']}")
    st.write("---")

# --- Вывод новостей из Telegram ---
st.subheader(f"Найдено новостей (Telegram): {len(filtered_telegram_news)}")
for item in filtered_telegram_news:
    st.markdown(f"**Канал:** [{item['channel']}]({item['channel']})")
    st.markdown(f"**Сообщение:** {item['text']}")
    st.markdown(f"**Дата:** {item['date']}")
    st.write("---")

# --- Информация о приложении ---
st.sidebar.info(
    """
    Это приложение создано для агрегирования новостей из регионов Калмыкия и Ингушетия.
    Источники: RSS-ленты и Telegram-каналы через Telegram API.
    """
)

import tweepy
import feedparser
import os
import random
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Autenticación con Twitter API v2
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

# Lista de feeds RSS
feeds = [
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.theblock.co/feeds/rss",
    "https://bitcoinmagazine.com/.rss/full/",
    "https://cryptoslate.com/feed/",
    "https://www.newsbtc.com/feed/"
]

# Intentar encontrar un feed con entradas
max_attempts = 3
attempts = 0

while attempts < max_attempts:
    selected_feed = random.choice(feeds)
    print(f"🔄 Probando feed: {selected_feed}")
    feed = feedparser.parse(selected_feed)
    if feed.entries:
        print(f"✅ Entradas encontradas en {selected_feed}")
        break
    else:
        print(f"⚠️ No se encontraron entradas en {selected_feed}. Reintentando...")
        attempts += 1

if not feed.entries:
    print("❌ No se encontraron entradas en ninguno de los feeds. Abortando.")
    exit()

# Tomar la noticia más reciente
entry = feed.entries[0]

title = entry.title
summary = entry.summary if hasattr(entry, 'summary') else ''
url = entry.link

# Hashtags simples por palabras clave
hashtags = []

if "bitcoin" in title.lower():
    hashtags.append("#Bitcoin")
if "ethereum" in title.lower():
    hashtags.append("#Ethereum")
if "defi" in title.lower():
    hashtags.append("#DeFi")
if "nft" in title.lower():
    hashtags.append("#NFT")
if not hashtags:
    hashtags.append("#Crypto")

hashtags_text = " ".join(hashtags)

# Crear el texto del tweet
from transformers import pipeline

# Preparar el texto original
text_to_summarize = f"{title}\n\n{summary}"

# Cargar el pipeline de resumen (solo se hace una vez al principio)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Generar el resumen
huggingface_summary = summarizer(
    text_to_summarize,
    max_length=60,
    min_length=20,
    do_sample=False
)[0]['summary_text']

# Hashtags simples por palabras clave
hashtags = []

if "bitcoin" in title.lower():
    hashtags.append("#Bitcoin")
if "ethereum" in title.lower():
    hashtags.append("#Ethereum")
if "defi" in title.lower():
    hashtags.append("#DeFi")
if "nft" in title.lower():
    hashtags.append("#NFT")
if not hashtags:
    hashtags.append("#Crypto")

hashtags_text = " ".join(hashtags)

# Crear el tweet final con el resumen
tweet_text = f"{huggingface_summary}\n\n{hashtags_text}\n{url}"

# Limitar longitud máxima de tweet
if len(tweet_text) > 280:
    allowed_summary_length = 280 - len(hashtags_text) - len(url) - 10
    huggingface_summary = huggingface_summary[:allowed_summary_length] + "..."
    tweet_text = f"{huggingface_summary}\n\n{hashtags_text}\n{url}"

# Publicar el tweet
response = client.create_tweet(
    text=tweet_text
)

print("✅ Tweet publicado. ID:", response.data["id"])

import tweepy
import feedparser
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear cliente v2
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

# Leer el feed RSS
feed = feedparser.parse("https://cointelegraph.com/rss")

# Verificar que hay noticias
if not feed.entries:
    print("⚠️ No se encontraron entradas en el feed.")
    exit()

# Tomar la noticia más reciente
entry = feed.entries[0]
title = entry.title
url = entry.link

# Crear el texto del tweet
tweet_text = f"{title}\n{url}\n#Crypto #Blockchain"

# Publicar el tweet
response = client.create_tweet(
    text=tweet_text
)

print("✅ Tweet publicado. ID:", response.data["id"])

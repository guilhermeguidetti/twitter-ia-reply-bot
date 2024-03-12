import tweepy
import google.generativeai as genai

# Configuração da API do Google Gemini
GOOGLE_API_KEY = "AIAPIKEYyDV5Ps"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def gerar_resposta_gemini(texto):
    prompt = f"Imagine que você está respondendo informalmente o seguinte tweet e dando sua opinião com humor: {texto}"
    response = model.generate_content(prompt)
    print(response.text)
    return response.text

def carregar_respondidos(arquivo):
    try:
        with open(arquivo, "r") as f:
            return [linha.strip() for linha in f]
    except FileNotFoundError:
        return []

def salvar_respondido(arquivo, tweet_id):
    with open(arquivo, "a") as f:
        f.write(f"{tweet_id}\n")

arquivo_respondidos = "respondidos.txt"
respondidos = carregar_respondidos(arquivo_respondidos)

consumer_key = 'cy1wUnRAPIKEYFQ6MTpjaQ'
consumer_secret = 'rncLay5p5APIKEYwucXcNHJSX'
access_token = '156586519377APIKEYnqQTgj'
access_token_secret = '1HjOKxAPIKEYCVPl'

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamingClient):
    def on_status(self, status):
        try:
            tweet_id = str(status.id)
            if tweet_id in respondidos or hasattr(status, 'retweeted_status'):
                return

            tweet_text = status.text
            user_name = status.user.screen_name

            print(f"Respondendo ao tweet de @{user_name} com ID {tweet_id} e texto: {tweet_text}")
            api.create_favorite(tweet_id)
            api.retweet(tweet_id)

            resposta = gerar_resposta_gemini(tweet_text)
            api.update_status(status=f'@{user_name} {resposta}', in_reply_to_status_id=tweet_id)

            respondidos.append(tweet_id)
            salvar_respondido(arquivo_respondidos, tweet_id)
        
        except Exception as e:
            print(f"Erro: {e}")

stream_listener = MyStreamListener('AAAAAAAAAAAAAAAAAAAAABwGswEAAPIKEY%3Du8w4dQIsGtGpbuOeIOBjQsDJaki4d2j1dp5zEHxDSjOsHgUg6Z')
stream_listener.add_rules(tweepy.StreamRule("from:usuario1000"))
stream_listener.filter()

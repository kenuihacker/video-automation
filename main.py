import os
import time
import requests
from gtts import gTTS
from moviepy.editor import *
from google_auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Acessando as variáveis de ambiente
TIKTOK_CLIENT_KEY = os.getenv('TIKTOK_CLIENT_KEY')
TIKTOK_CLIENT_SECRET = os.getenv('TIKTOK_CLIENT_SECRET')
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
UNSPLASH_SECRET_KEY = os.getenv('UNSPLASH_SECRET_KEY')

# Função para gerar narração do texto
def generate_narration(text):
    tts = gTTS(text=text, lang='pt')
    tts.save("narration.mp3")
    return "narration.mp3"

# Função para baixar uma imagem do Unsplash
def download_image():
    url = f"https://api.unsplash.com/photos/random?client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    data = response.json()
    image_url = data[0]['urls']['regular']
    img_data = requests.get(image_url).content
    with open('image.jpg', 'wb') as handler:
        handler.write(img_data)

# Função para criar um vídeo
def create_video():
    # Baixar imagem do Unsplash
    download_image()

    # Adicionar a imagem como base para o vídeo
    image = ImageClip("image.jpg")
    image = image.set_duration(10)

    # Adicionar a narração
    narration = AudioFileClip("narration.mp3")
    video = image.set_audio(narration)

    # Salvar o vídeo
    video.write_videofile("final_video.mp4", fps=24)

# Função para enviar o vídeo para o Google Drive
def upload_to_drive():
    # Autenticando no Google Drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Cria um servidor local para autenticação OAuth2
    drive = GoogleDrive(gauth)

    # Enviar o vídeo para o Google Drive
    video_file = drive.CreateFile({'title': 'final_video.mp4'})
    video_file.Upload()

    print("Vídeo enviado para o Google Drive com sucesso!")

# Função para monitorar e criar vídeos periodicamente
def main():
    text = "Aqui está um vídeo automatizado criado com Python."
    generate_narration(text)
    create_video()

    # Enviar para o Google Drive
    upload_to_drive()

if __name__ == "__main__":
    while True:
        main()
        time.sleep(3600)  # Espera 1 hora antes de rodar novamente

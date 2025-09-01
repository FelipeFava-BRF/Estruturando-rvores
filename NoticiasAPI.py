
import os
from dotenv import load_dotenv
import requests

def carregar_api_key():
    try:
        # Carrega variáveis do .env        
        load_dotenv()
        # Acessa a chave em específico     
        api_key = os.getenv("chave_NoticiasAPI")

        if not api_key:
            raise ValueError("Chave API não encontrada em .env")
        return api_key
    except Exception as e:
        print(f"Erro ao carregar a chave da API: {e}")
        return None

def buscar_noticias():
    API_KEY = carregar_api_key()

    if not API_KEY:
        print("Não foi possível carregar a chave da API")
        return
    
    url = "https://newsapi.org/v2/everything"  

    tema = input("Digite um tema para buscar notícias (ou pressione Enter para ver sugestões): ")
    if not tema:
        sugestoes = ["tecnologia", "saúde", "economia", "educação", "esportes", "meio ambiente"]
        print("\nSugestões de temas:")
        
        for i, sugestao in enumerate(sugestoes, 1):
            print(f"{i}. {sugestao}")

        escolha = input("Escolha um número ou digite um novo tema: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(sugestoes):
            tema = sugestoes[int(escolha) - 1]
        else:
            tema = escolha

    idioma = input("Digite o idioma (ex: pt, en, es) ou pressione Enter para qualquer idioma: ").strip()
    data = input("Digite a data mínima de publicação (formato YYYY-MM-DD) ou pressione Enter para ignorar: ").strip()
 
    # "language": "pt",  # idioma
    params = {
        "q": tema,
        "sortBy": "publishedAt",
        "apikey": API_KEY
    }

    if idioma:
        params["language"] = idioma
    if data:
        params["from"] = data

    resposta = requests.get(url, params=params)

    if resposta.status_code == 200:
        noticias = resposta.json()
        print(f"\nForam encontradas {noticias['totalResults']} notícias sobre '{tema}':\n")

        for artigo in noticias["articles"][:10]:
            print(f"Título: {artigo['title']}")
            print(f"Fonte: {artigo['source']['name']}")
            print(f"Publicado em: {artigo['publishedAt']}")
            print(f"Link: {artigo['url']}\n")
    else:
        print(f"Erro: {resposta.status_code} - {resposta.text}")

#executa a função principal
buscar_noticias()

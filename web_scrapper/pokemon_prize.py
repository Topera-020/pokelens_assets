import os
import requests

# Diretório onde as imagens serão salvas
pasta_destino = "imagens_prize_series"
os.makedirs(pasta_destino, exist_ok=True)

# URL base
url_base = "https://d1wx537rtdixyy.cloudfront.net/expansions/series7/en-us/OP_Prize_SE7_EN_{}-2x.png"

# Loop de 1 a 96
for i in range(1, 97):
    url = url_base.format(i)
    nome_arquivo = f"PSE7-{i}.png"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)

    try:
        print(f"Baixando {url}...")
        resposta = requests.get(url, timeout=10)
        if resposta.status_code == 200:
            with open(caminho_completo, "wb") as f:
                f.write(resposta.content)
            print(f"Salvo como {caminho_completo}")
        else:
            print(f"Falha ao baixar (status {resposta.status_code}): {url}")

    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

print("Download concluído.")

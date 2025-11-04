import os

# Caminho da pasta onde estão os arquivos
pasta = r"D:\Thales\Documentos\Pokelens\pokelens_web\pokelens_assets\cartas\PSE7"

for nome_arquivo in os.listdir(pasta):
    if "PPPS6-" in nome_arquivo:
        novo_nome = nome_arquivo.replace("PPPS6-", "PPPS7-")
        caminho_antigo = os.path.join(pasta, nome_arquivo)
        caminho_novo = os.path.join(pasta, novo_nome)
        os.rename(caminho_antigo, caminho_novo)
        print(f"Renomeado: {nome_arquivo} -> {novo_nome}")

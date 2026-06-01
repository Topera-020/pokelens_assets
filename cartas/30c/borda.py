from PIL import Image
import numpy as np
import os

def cortar_borda_preta(arquivo):
    img = Image.open(arquivo).convert("RGB")
    arr = np.array(img)

    mascara = np.any(arr > 10, axis=2)

    if not mascara.any():
        return

    ys, xs = np.where(mascara)

    esquerda = xs.min()
    direita = xs.max() + 1
    topo = ys.min()
    baixo = ys.max() + 1

    img.crop((esquerda, topo, direita, baixo)).save(arquivo)

pasta = r"pokelens_assets\cartas\30c"

for raiz, _, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        if arquivo.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            caminho = os.path.join(raiz, arquivo)

            try:
                cortar_borda_preta(caminho)
                print(f"OK: {caminho}")
            except Exception as e:
                print(f"ERRO: {caminho} -> {e}")

print("Concluído")
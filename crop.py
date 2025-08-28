import cv2
import numpy as np
import os

# Caminho das imagens originais
input_dir = r"C:\\xampp\\htdocs\\site_pokelens\\assets\\sleeves"
# Caminho para salvar as imagens processadas
output_dir = r"C:\\xampp\\htdocs\\site_pokelens\\assets\\sleeves_cropped"

# Tamanho máximo para a largura ou altura
max_width = 200
max_height = 200

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        file_path = os.path.join(input_dir, filename)
        img = cv2.imread(file_path)

        if img is None:
            print(f"Erro ao ler {filename}")
            continue

        # converte para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # máscara de pixels não brancos (assumindo fundo branco ≥ 240)
        _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

        # encontra contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print(f"Nenhum objeto detectado em {filename}")
            continue

        # pega bounding box do maior contorno
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        # recorta a imagem original
        cropped = img[y:y+h, x:x+w]

        # calcula escala para manter o aspect ratio
        scale = min(max_width / w, max_height / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        # redimensiona mantendo proporção
        resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        # salva a imagem processada
        save_path = os.path.join(output_dir, filename)
        cv2.imwrite(save_path, resized)
        print(f"Processada: {filename} ({new_w}x{new_h})")

print("Todas as imagens foram processadas!")




#https://www.ligapokemon.com.br/?view=prod/view&pcode=132213

#https://www.ligapokemon.com.br/?view=cards%2Fsearch&tipo=1&card=categ%3D41+searchprod%3D1
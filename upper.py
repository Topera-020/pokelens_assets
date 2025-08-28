import cv2
import numpy as np
import os

# Pasta original
input_dir = r"C:\xampp\htdocs\site_pokelens\assets\sleeves"
# Pasta de saída
output_dir = r"C:\xampp\htdocs\site_pokelens\assets\sleeves_processed"
os.makedirs(output_dir, exist_ok=True)

# Escala máxima para ampliar
scale_factor = 2

# Kernel de nitidez
sharpen_kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        file_path = os.path.join(input_dir, filename)
        img = cv2.imread(file_path)

        if img is None:
            print(f"Erro ao ler {filename}")
            continue

        # converte para cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # máscara de pixels não brancos
        _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

        # contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print(f"Nenhum objeto detectado em {filename}")
            continue

        # bounding box do maior contorno
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        # recorta a imagem
        cropped = img[y:y+h, x:x+w]

        # redimensiona mantendo proporção
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)
        resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        # aplica sharpen
        sharpened = cv2.filter2D(resized, -1, sharpen_kernel)

        # salva
        save_path = os.path.join(output_dir, filename)
        cv2.imwrite(save_path, sharpened)
        print(f"Processada: {filename} -> {save_path}")

print("Todas as imagens foram processadas e salvas na pasta secundária!")

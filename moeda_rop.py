import cv2
import numpy as np
import os

input_dir = r"C:\xampp\htdocs\site_pokelens\assets\moedas"
output_dir = r"C:\xampp\htdocs\site_pokelens\assets\moedas_processed"
os.makedirs(output_dir, exist_ok=True)

final_size = 200  # tamanho máximo do lado

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        file_path = os.path.join(input_dir, filename)
        img = cv2.imread(file_path)

        if img is None:
            print(f"Erro ao ler {filename}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # máscara para identificar contorno externo da moeda
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        # aplica morfologia para fechar buracos internos
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # encontra contornos
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print(f"Nenhuma moeda detectada em {filename}")
            continue

        # pega contorno maior (moeda)
        c = max(contours, key=cv2.contourArea)

        # cria máscara do contorno externo
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [c], -1, 255, thickness=-1)  # preenche contorno
        mask = cv2.GaussianBlur(mask, (7,7), 0)  # suaviza borda

        # cria imagem BGRA
        b, g, r = cv2.split(img)
        alpha = mask
        rgba = cv2.merge([b, g, r, alpha])

        # redimensiona mantendo proporção
        h, w = rgba.shape[:2]
        scale = final_size / max(w, h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(rgba, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        # salva como PNG para manter transparência
        save_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".png")
        cv2.imwrite(save_path, resized)
        print(f"Processada: {filename} -> {save_path} ({new_w}x{new_h})")

print("Todas as moedas foram processadas com fundo transparente e borda suavizada!")

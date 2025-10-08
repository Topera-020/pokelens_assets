from PIL import Image
import os

def convert_all_jpg_to_png(input_folder: str, output_folder: str):
    # Cria a pasta de saída se não existir
    os.makedirs(output_folder, exist_ok=True)

    # Lista todos os arquivos na pasta de entrada
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            input_path = os.path.join(input_folder, filename)
            output_name = os.path.splitext(filename)[0] + ".png"
            output_path = os.path.join(output_folder, output_name)

            try:
                img = Image.open(input_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, 'PNG')
                print(f"Convertido: {filename} → {output_name}")
            except Exception as e:
                print(f"Erro ao converter {filename}: {e}")

# Exemplo de uso
input_folder = "sleeves"
output_folder = "sleeves"
convert_all_jpg_to_png(input_folder, output_folder)

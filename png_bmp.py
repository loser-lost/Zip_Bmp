from PIL import Image
import os
import zipfile
import shutil
from google.colab import files

# Função para converter e salvar uma imagem como BMP
def convert_to_bmp(image_path):
    try:
        img = Image.open(image_path)
        bmp_path = image_path.replace(os.path.splitext(image_path)[1], '.bmp')  # Substitui a extensão para BMP
        img.save(bmp_path, 'BMP')
        print(f"Imagem {image_path} convertida para BMP: {bmp_path}")
        return bmp_path
    except Exception as e:
        print(f"Erro ao converter a imagem {image_path}: {e}")
        return None

# Faz o upload do arquivo zip contendo as imagens
uploaded = files.upload()

# Extrai o arquivo zip para a pasta '/content/imagens'
for zip_filename in uploaded.keys():
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall('/content/imagens')  # Extrai para a pasta '/content/imagens'
        print(f"Arquivo {zip_filename} extraído com sucesso.")

# Converte as imagens para BMP na pasta '/content/imagens' e salva em uma lista
bmp_images = []
folder_path = '/content/imagens'
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(root, file)
            bmp_path = convert_to_bmp(image_path)
            if bmp_path:
                bmp_images.append(bmp_path)

# Cria um arquivo ZIP com as imagens BMP
if bmp_images:
    zip_filename_no_extension = os.path.splitext(list(uploaded.keys())[0])[0]
    new_zip_filename = f"{zip_filename_no_extension}_bmp.zip"

    with zipfile.ZipFile(new_zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for bmp_image in bmp_images:
            zipf.write(bmp_image, os.path.basename(bmp_image))  # Adiciona os arquivos ao ZIP
    print(f"Arquivo ZIP com imagens BMP criado com sucesso: {new_zip_filename}")
    # Exclui a pasta 'imagens'
    shutil.rmtree('/content/imagens')
    # Faz o download do arquivo ZIP contendo as imagens BMP
    #files.download(new_zip_filename)

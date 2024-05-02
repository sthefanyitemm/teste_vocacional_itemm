import random
from PIL import Image, ImageDraw

def generate_captcha(image_paths):
    """
    Gera um Captcha com uma imagem aleatória da lista de caminhos de imagem fornecida.
    
    Args:
        image_paths (list): Lista de caminhos de imagem possíveis.
        
    Returns:
        PIL.Image.Image: Imagem do Captcha gerado.
    """
    # Seleciona aleatoriamente uma imagem
    image_path = random.choice(image_paths)

    # Carrega a imagem selecionada
    img = Image.open(image_path)

    # Cria um objeto ImageDraw para desenhar na imagem
    draw = ImageDraw.Draw(img)

    return img

# Exemplo de uso
image_paths = ["app/src/static/car.png", "app/src/static/cat.png", "app/src/static/tree.png", "app/src/static/apple.png"]  # Adicione mais imagens conforme necessário
captcha_image = generate_captcha(image_paths)

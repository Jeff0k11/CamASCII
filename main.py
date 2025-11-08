import cv2
import numpy as np
import os
import sys

# String de caracteres ASCII ordenados do mais escuro ao mais claro
# Quanto mais denso o caractere, mais "claro" ele representa
# Versão ULTRA DETALHADA para máximo contraste (92 caracteres)
ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# Versão extendida
# ASCII_CHARS = " .`-_':,;^=+/\"|)\\<>)iv%xclrs{*}I?!][1taeo7zjLunT#JCwFG5S2&8%B@$"

# Versão média
# ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# Versão simplificada
# ASCII_CHARS = " .:-=+*#%@"


def resize_image(image, new_width=150, new_height=None):
    """
    Redimensiona a imagem.
    - Se new_height for None: mantém a proporção (com compensação para caracteres) usando apenas new_width.
    - Se new_height for fornecido: redimensiona exatamente para (new_width, new_height).
    """
    height, width = image.shape
    if new_height is None:
        aspect_ratio = height / width
        # Multiplica por 0.55 para compensar a proporção dos caracteres
        new_height = int(new_width * aspect_ratio * 0.55)

    # cv2.resize espera (width, height)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image


def grayscale_to_ascii(image):
    """
    Converte uma imagem em escala de cinza para arte ASCII.
    """
    ascii_art = []
    
    for row in image:
        ascii_row = ""
        for pixel_value in row:
            # Mapeia o valor do pixel (0-255) para o índice do caractere ASCII
            ascii_index = int((pixel_value / 255) * (len(ASCII_CHARS) - 1))
            ascii_row += ASCII_CHARS[ascii_index]
        ascii_art.append(ascii_row)
    
    return ascii_art


def ascii_to_image(ascii_art, char_width=6, char_height=10):
    """
    Converte arte ASCII em uma imagem OpenCV.
    """
    if not ascii_art:
        return None
    
    # Calcula dimensões da imagem
    num_rows = len(ascii_art)
    num_cols = len(ascii_art[0]) if ascii_art else 0
    
    img_width = num_cols * char_width
    img_height = num_rows * char_height
    
    # Cria uma imagem preta
    image = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    
    # Configurações de fonte
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.3
    font_thickness = 1
    color = (255, 255, 255)  # Branco
    
    # Desenha cada caractere
    for i, row in enumerate(ascii_art):
        for j, char in enumerate(row):
            x = j * char_width
            y = (i + 1) * char_height - 2
            cv2.putText(image, char, (x, y), font, font_scale, color, font_thickness, cv2.LINE_AA)
    
    return image


def main():
    # Inicializa a captura de vídeo da webcam (0 = webcam padrão)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erro: Não foi possível acessar a webcam!")
        return
    
    print("Iniciando captura ASCII da webcam...")
    print("Pressione 'q' na janela para sair\n")
    
    # Configurações para exibição em tela cheia Full HD
    TARGET_SCREEN_WIDTH = 1920
    TARGET_SCREEN_HEIGHT = 1080
    # Largura/altura (em pixels) de cada caractere na imagem final
    CHAR_WIDTH = 6
    CHAR_HEIGHT = 10

    # Cria janelas para exibir. A janela ASCII será configurada como fullscreen.
    cv2.namedWindow('Webcam Original', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('ASCII Art', cv2.WINDOW_NORMAL)
    # Define a janela ASCII como fullscreen (padrão Full HD target)
    try:
        cv2.setWindowProperty('ASCII Art', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    except Exception:
        # Alguns backends do OpenCV podem não suportar essa propriedade; não é crítico.
        pass
    
    try:
        while True:
            # Captura frame por frame
            ret, frame = cap.read()
            
            if not ret:
                print("Erro ao capturar frame!")
                break
            
            # Espelha horizontalmente o frame para que movimentos à esquerda
            # apareçam à direita (mirror), conforme solicitado
            frame = cv2.flip(frame, 1)

            # Mostra o frame original (já espelhado)
            cv2.imshow('Webcam Original', frame)

            # Converte para escala de cinza
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Redimensiona fixamente para 256x256 conforme solicitado
            resized_frame = resize_image(gray_frame, new_width=256, new_height=256)
            
            # Converte para ASCII
            ascii_art = grayscale_to_ascii(resized_frame)
            
            # Converte ASCII para imagem usando as dimensões do caractere
            ascii_image = ascii_to_image(ascii_art, char_width=CHAR_WIDTH, char_height=CHAR_HEIGHT)
            
            if ascii_image is not None:
                # Mostra a arte ASCII na janela
                cv2.imshow('ASCII Art', ascii_image)
            
            # Verifica se 'q' foi pressionado
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n\nEncerrando...")
    
    finally:
        # Libera a captura e fecha janelas
        cap.release()
        cv2.destroyAllWindows()
        print("Captura finalizada!")


if __name__ == "__main__":
    main()

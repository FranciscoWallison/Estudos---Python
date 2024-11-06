import cv2
import pyautogui
import numpy as np
import pytesseract
import mss
import os
import time

# Defina o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\my_bots\tl\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'D:\my_bots\tl\Tesseract-OCR\tessdata'

# Função para capturar tela e localizar sequência de texto
def find_and_move_to_text(target_text, region=None, interval=0.5):
    target_words = target_text.lower().split()  # Divide o texto-alvo em palavras
    with mss.mss() as sct:
        # Define a região de captura (opcional)
        monitor = sct.monitors[1] if region is None else region

        while True:
            # Captura a tela na região definida
            screenshot = np.array(sct.grab(monitor))
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            # Executa OCR com configuração para melhorar a precisão
            ocr_result = pytesseract.image_to_data(
                gray, config="--psm 6", output_type=pytesseract.Output.DICT
            )

            # Verifica a sequência das palavras no OCR
            match_index = 0  # Índice para acompanhar as palavras da sequência-alvo
            found_positions = []  # Armazena as coordenadas de cada palavra encontrada

            for i, text in enumerate(ocr_result['text']):

                if match_index < len(target_words) and target_words[match_index] in text.lower():
                    # Armazena as coordenadas da palavra correspondente
                    x, y, w, h = (ocr_result['left'][i], ocr_result['top'][i],
                                  ocr_result['width'][i], ocr_result['height'][i])
                    found_positions.append((x + w // 2, y + h // 2))
                    
                    match_index += 1  # Avança para a próxima palavra
                    if match_index == len(target_words):
                        # Se todas as palavras foram encontradas na ordem correta
                        center_x, center_y = found_positions[0]  # Posição da primeira palavra encontrada
                        pyautogui.moveTo(center_x, center_y, duration=0.5)
                        print(f"Texto 54564654 encontrado e cursor movido para ({center_x}, {center_y})")
                        return True

            print(f"Texto 54564654 não encontrado, tentando novamente...")
            time.sleep(interval)  # Intervalo antes da próxima captura

# Exemplo de uso
find_and_move_to_text('Ceifador Violento', interval=1)

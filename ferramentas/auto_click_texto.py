import tkinter as tk
from tkinter import filedialog
import cv2
import pyautogui
import numpy as np
import pytesseract
import mss
import os
import threading
import time
from PIL import ImageGrab

# Defina o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\my_bots\te\Tesseract-OCR\tesseract.exe'

# Defina o caminho para o diretório 'tessdata'
os.environ['TESSDATA_PREFIX'] = r'D:\my_bots\te\Tesseract-OCR\tessdata'
# Função para capturar a tela e localizar o texto
def find_and_move_to_text(target_text):
    # Captura uma imagem da tela
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)

    # Converte a imagem para escala de cinza para o OCR
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    # Realiza o OCR na imagem capturada
    ocr_result = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
    
    # Procura pelo texto desejado
    for i, text in enumerate(ocr_result['text']):
        if target_text.lower() in text.lower():
            x, y, w, h = (ocr_result['left'][i], ocr_result['top'][i], 
                          ocr_result['width'][i], ocr_result['height'][i])
            # Calcula a posição central do texto encontrado
            center_x, center_y = x + w // 2, y + h // 2
            
            # Move o cursor para o centro do texto
            pyautogui.moveTo(center_x, center_y, duration=0.5)
            print(f"Texto encontrado e cursor movido para ({center_x}, {center_y})")
            return True  # Texto encontrado e cursor movido
    print("Texto não encontrado")
    return False  # Texto não encontrado

# Uso da função: substitua 'Texto Alvo' pelo texto que deseja identificar
find_and_move_to_text('Ceifador')

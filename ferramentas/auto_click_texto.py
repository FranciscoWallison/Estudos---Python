import cv2
import pyautogui
import numpy as np
import pytesseract
import mss
import os
import time
import tkinter as tk
from tkinter import simpledialog

# Defina o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\my_bots\tl\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'D:\my_bots\tl\Tesseract-OCR\tessdata'

# Fator de escala para redimensionamento
scale_percent = 150

# Variável global para armazenar a região de captura
region_of_interest = None

# Função para capturar tela e localizar sequência de texto
def find_and_move_to_text(text_list, region=None, interval=0.5, max_attempts=5):
    current_index = 0  # Começa no primeiro texto da lista

    with mss.mss() as sct:
        monitor = sct.monitors[1] if region is None else region

        while True:
            # Captura a tela na região definida
            screenshot = np.array(sct.grab(monitor))
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            # Pré-processamento: Aumenta o contraste e redimensiona a imagem para melhorar o OCR
            _, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

            # Redimensiona a imagem para aumentar a precisão
            width = int(gray.shape[1] * scale_percent / 100)
            height = int(gray.shape[0] * scale_percent / 100)
            gray_resized = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LINEAR)

            # Configuração do OCR
            ocr_result = pytesseract.image_to_data(
                gray_resized, config="--oem 3 --psm 6", output_type=pytesseract.Output.DICT
            )

            attempts = 0
            while attempts < max_attempts:
                target_text = text_list[current_index][::-1]  # Desinverte o texto
                target_words = target_text.lower().split()
                found_positions = []
                match_index = 0

                for i, text in enumerate(ocr_result['text']):
                    if match_index < len(target_words) and target_words[match_index] in text.lower():
                        # Ajusta as coordenadas para a escala original
                        x = int(ocr_result['left'][i] * 100 / scale_percent)
                        y = int(ocr_result['top'][i] * 100 / scale_percent)
                        w = int(ocr_result['width'][i] * 100 / scale_percent)
                        h = int(ocr_result['height'][i] * 100 / scale_percent)
                        found_positions.append((x + w // 2, y + h // 2))
                        match_index += 1

                        if match_index == len(target_words):
                            center_x = monitor['left'] + found_positions[0][0]
                            center_y = monitor['top'] + found_positions[0][1]
                            pyautogui.moveTo(center_x, center_y, duration=0.5)
                            print(f"Texto '{target_text}' encontrado e cursor movido para ({center_x}, {center_y})")
                            return True

                attempts += 1
                print(f"Tentativa {attempts} para '{target_text}' falhou. Tentando novamente...")
                time.sleep(interval)

            # Passa para o próximo texto ou volta ao início se não encontrar nenhum
            current_index = (current_index + 1) % len(text_list)
            print(f"Não encontrou o texto. Mudando para o próximo da lista de prioridades...")

# Função para criar a interface de entrada e seleção de região
def get_text_priorities():
    global region_of_interest

    # Cria a janela principal
    root = tk.Tk()
    root.title("Configuração do OCR")

    text_priorities = []

    # Função para desenhar a região de interesse
    def select_region():
        root.withdraw()  # Oculta a janela principal durante a seleção

        # Espera um pouco para evitar capturar o clique do botão
        time.sleep(0.5)

        # Captura a tela inteira
        screenshot = pyautogui.screenshot()
        screen_width, screen_height = screenshot.size

        # Cria uma janela de tela cheia para desenhar a região
        select_root = tk.Toplevel()
        select_root.overrideredirect(True)
        select_root.attributes('-alpha', 0.3)  # Janela semi-transparente
        select_root.geometry(f"{screen_width}x{screen_height}+0+0")

        canvas = tk.Canvas(select_root, width=screen_width, height=screen_height)
        canvas.pack()

        coords = {}

        def on_click(event):
            coords['x_start'] = event.x
            coords['y_start'] = event.y

        def on_drag(event):
            canvas.delete("selection")
            x_start = coords.get('x_start', event.x)
            y_start = coords.get('y_start', event.y)
            canvas.create_rectangle(x_start, y_start, event.x, event.y, outline='red', tag="selection")

        def on_release(event):
            coords['x_end'] = event.x
            coords['y_end'] = event.y
            select_root.destroy()

            x_start = coords['x_start']
            y_start = coords['y_start']
            x_end = coords['x_end']
            y_end = coords['y_end']

            # Define o formato esperado pela função find_and_move_to_text
            region_of_interest = {
                "left": min(x_start, x_end),
                "top": min(y_start, y_end),
                "width": abs(x_end - x_start),
                "height": abs(y_end - y_start),
            }
            print("Região de interesse definida:", region_of_interest)
            root.deiconify()  # Exibe novamente a janela principal

        canvas.bind("<ButtonPress-1>", on_click)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

        select_root.mainloop()

    # Adiciona um botão para iniciar a seleção de região
    region_button = tk.Button(root, text="Selecionar Região de Captura", command=select_region)
    region_button.pack(pady=10)

    # Função para adicionar textos à lista
    def add_text():
        user_input = text_entry.get()
        if user_input:
            text_priorities.append(user_input[::-1])  # Adiciona o texto invertido para ofuscação
            listbox.insert(tk.END, user_input)
            text_entry.delete(0, tk.END)

    # Campo de entrada de texto
    text_entry = tk.Entry(root, width=40)
    text_entry.pack(pady=5)

    add_button = tk.Button(root, text="Adicionar Texto", command=add_text)
    add_button.pack(pady=5)

    # Lista para mostrar os textos adicionados
    listbox = tk.Listbox(root, width=50)
    listbox.pack(pady=5)

    # Botão para finalizar a entrada e iniciar a busca
    def start_search():
        root.destroy()

    start_button = tk.Button(root, text="Iniciar Busca", command=start_search)
    start_button.pack(pady=10)

    root.mainloop()
    return text_priorities

# Obter os textos de prioridade e a região de interesse do usuário
text_priority_list = get_text_priorities()

# Verifica se a lista não está vazia antes de iniciar a busca
if text_priority_list:
    find_and_move_to_text(text_priority_list, region=region_of_interest, interval=1)
else:
    print("Nenhum texto foi inserido.")

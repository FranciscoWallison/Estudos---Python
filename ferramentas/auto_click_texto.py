import tkinter as tk
import pyautogui
import pytesseract
import cv2
import numpy as np
import time
import os
import threading
from PIL import Image
import random

# Configuração do caminho do Tesseract e do OpenCV
pytesseract.pytesseract.tesseract_cmd = r'D:\my_bots\t\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'D:\my_bots\t\Tesseract-OCR\tessdata'

class TextSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot de Combate a Mobs")

        # Lista de textos a serem procurados
        self.text_list = []
        self.load_texts_from_file()

        # Área para adicionar textos
        tk.Label(root, text="Adicionar texto à lista de busca:").pack(pady=5)
        self.entry_text = tk.Entry(root)
        self.entry_text.pack(pady=5)
        tk.Button(root, text="Adicionar Texto", command=self.add_text).pack(pady=5)

        # Área para exibir textos cadastrados
        tk.Label(root, text="Textos Cadastrados:").pack(pady=5)
        self.text_display = tk.Text(root, height=5, width=50, state='disabled')
        self.text_display.pack(pady=5)
        self.update_text_display()

        # Botões para selecionar região e buscar texto
        tk.Button(root, text="Selecionar Região", command=self.start_region_selection).pack(pady=10)
        tk.Button(root, text="Iniciar Bot de Combate", command=self.start_combat_thread).pack(pady=10)

        # Área de logs
        tk.Label(root, text="Logs de Busca:").pack(pady=5)
        self.log_text = tk.Text(root, height=10, width=50, state='disabled')
        self.log_text.pack(pady=5)

        # Variáveis de controle para seleção de região
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.rect = None
        self.selecting = False

    def log_message(self, message):
        # Função para exibir mensagens na área de log
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def add_text(self):
        # Adiciona um texto à lista e atualiza a exibição
        text = self.entry_text.get().strip()
        if text:
            self.text_list.append(text)
            self.save_texts_to_file()
            self.update_text_display()
            self.entry_text.delete(0, tk.END)
            self.log_message(f"Texto '{text}' adicionado à lista de busca.")

    def update_text_display(self):
        # Atualiza a exibição dos textos cadastrados
        self.text_display.config(state='normal')
        self.text_display.delete(1.0, tk.END)
        for text in self.text_list:
            self.text_display.insert(tk.END, text + "\n")
        self.text_display.config(state='disabled')

    def save_texts_to_file(self):
        # Salva a lista de textos em um arquivo txt
        with open("text_list.txt", "w") as file:
            for text in self.text_list:
                file.write(text + "\n")

    def load_texts_from_file(self):
        # Carrega a lista de textos de um arquivo txt
        if os.path.exists("text_list.txt"):
            with open("text_list.txt", "r") as file:
                self.text_list = [line.strip() for line in file if line.strip()]

    def start_region_selection(self):
        # Cria uma janela de tela cheia para a seleção de região
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes("-fullscreen", True)
        self.selection_window.attributes("-alpha", 0.3)
        self.selection_window.bind("<Button-1>", self.on_mouse_down)
        self.selection_window.bind("<B1-Motion>", self.on_mouse_drag)
        self.selection_window.bind("<ButtonRelease-1>", self.on_mouse_up)

    def on_mouse_down(self, event):
        # Início da seleção da região
        self.start_x, self.start_y = event.x, event.y
        self.selecting = True
        self.rect = tk.Canvas(self.selection_window, cursor="cross")
        self.rect.place(x=0, y=0, width=self.selection_window.winfo_screenwidth(), height=self.selection_window.winfo_screenheight())

    def on_mouse_drag(self, event):
        # Atualiza o retângulo conforme o mouse é arrastado
        if self.selecting:
            self.rect.delete("selection")
            self.end_x, self.end_y = event.x, event.y
            self.rect.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red", tag="selection")

    def on_mouse_up(self, event):
        # Finaliza a seleção de região
        self.selecting = False
        self.selection_window.destroy()

        # Corrige a posição e tamanho da região selecionada
        self.x1, self.y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        self.x2, self.y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        self.log_message(f"Região selecionada: ({self.x1}, {self.y1}) a ({self.x2}, {self.y2})")

    def start_combat_thread(self):
        # Inicia uma nova thread para o bot de combate a mobs
        combat_thread = threading.Thread(target=self.start_combat_bot)
        combat_thread.daemon = True
        combat_thread.start()

    def start_combat_bot(self):
        # Inicia o bot para combate a mobs
        while True:
            if self.search_and_attack():
                self.log_message("Iniciando novo ciclo de busca de mobs.")
            else:
                self.log_message("Todos os mobs da lista foram verificados. Reiniciando busca...")

    def search_and_attack(self):
        # Captura a região selecionada e busca os textos em sequência
        screenshot = pyautogui.screenshot(region=(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
        text_data = pytesseract.image_to_string(screenshot)

        for text in self.text_list:
            if text.lower() in text_data.lower():
                # Mover o cursor e realizar duplo clique
                text_boxes = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
                for i, word in enumerate(text_boxes["text"]):
                    if word.lower() == text.split()[0].lower():
                        x = self.x1 + text_boxes["left"][i]
                        y = self.y1 + text_boxes["top"][i]
                        pyautogui.moveTo(x, y)
                        pyautogui.doubleClick()
                        self.log_message(f"Texto '{text}' encontrado. Realizando duplo clique.")
                        time.sleep(0.5)

                        # Repete o ataque enquanto o monstro está focado
                        while self.check_for_monster_focus():
                            # Segurar a tecla "E" por 5 segundos
                            self.log_message("Atacando com a tecla 'E'.")
                            pyautogui.keyDown('e')
                            time.sleep(5)
                            pyautogui.keyUp('e')

                        # Se o monstro não está mais focado, reiniciar a busca
                        self.log_message("Monstro não encontrado. Reiniciando busca de novo alvo.")
                        self.simulate_mistake()
                        return False  # Procura um novo alvo

        return False  # Nenhum texto encontrado na lista

    def simulate_mistake(self):        
        mistake_key = str(random.randint(1, 4))

        pyautogui.press(mistake_key)
        # Pausa aleatória para simular o erro
        time.sleep(random.uniform(0.5, 1.5))
        pyautogui.press(mistake_key)

    def screenshot(self):
        screen = pyautogui.screenshot()
        screen = np.array(screen)
        return cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    
    def check_for_monster_focus(self):

        screen_gray = self.screenshot()
        
        monster_images_paths = [
            "path/to/monster_focused.png",
            "path/to/monster_focused_2.png",
            "path/to/monster_focused_4.png"
        ]

        templates = [cv2.imread(path, 0) for path in monster_images_paths]

        for template in templates:
            res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            if res.max() >= threshold:
                self.log_message(f"Monstro encontrado com pontuação de {res.max()}")
                return True
        return False

# Inicializa a interface gráfica
root = tk.Tk()
app = TextSearchApp(root)
root.mainloop()

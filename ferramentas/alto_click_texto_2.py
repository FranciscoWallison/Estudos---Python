import tkinter as tk
from tkinter import messagebox
import pyautogui
import pytesseract
from PIL import Image
import os

# Definindo caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\my_bots\Throne_and_Liberty_2\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'D:\my_bots\Throne_and_Liberty_2\Tesseract-OCR\tessdata'

class TextSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Busca de Texto na Tela")

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
        tk.Button(root, text="Buscar Texto", command=self.search_text).pack(pady=10)

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

    def search_text(self):
        # Captura a região selecionada e busca os textos em sequência
        try:
            screenshot = pyautogui.screenshot(region=(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
            text_data = pytesseract.image_to_string(screenshot)

            for text in self.text_list:
                if text.lower() in text_data.lower():
                    # Obtém as coordenadas aproximadas do texto encontrado
                    text_boxes = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
                    for i, word in enumerate(text_boxes["text"]):
                        if word.lower() == text.split()[0].lower():
                            x = self.x1 + text_boxes["left"][i]
                            y = self.y1 + text_boxes["top"][i]
                            pyautogui.moveTo(x, y)
                            self.log_message(f"Texto '{text}' encontrado. Cursor movido para posição ({x}, {y}).")
                            return
                    self.log_message(f"Texto '{text}' encontrado na região, mas posição exata não foi identificada.")
                    return

            self.log_message("Nenhum dos textos cadastrados foi encontrado.")
        except Exception as e:
            self.log_message(f"Erro: {str(e)}")

# Inicializa a interface gráfica
root = tk.Tk()
app = TextSearchApp(root)
root.mainloop()

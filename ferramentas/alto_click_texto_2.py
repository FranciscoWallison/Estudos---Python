import tkinter as tk
from tkinter import messagebox
import pyautogui
import pytesseract
from PIL import Image

# Configuração do caminho do Tesseract, se necessário
import os


# Definindo caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\my_bots\Throne_and_Liberty_2\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'D:\my_bots\Throne_and_Liberty_2\Tesseract-OCR\tessdata'


class TextSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Busca de Texto na Tela")

        # Variável para armazenar o texto a ser procurado
        self.target_text = tk.StringVar()

        # Interface para entrada de texto
        tk.Label(root, text="Texto a buscar:").pack(pady=5)
        tk.Entry(root, textvariable=self.target_text).pack(pady=5)

        # Botões para selecionar região e buscar texto
        tk.Button(root, text="Selecionar Região", command=self.start_region_selection).pack(pady=10)
        tk.Button(root, text="Buscar Texto", command=self.search_text).pack(pady=10)

        # Área de logs
        self.log_text = tk.Text(root, height=10, width=50, state='disabled')
        self.log_text.pack(pady=10)

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
        # Captura a região selecionada e busca o texto especificado
        try:
            screenshot = pyautogui.screenshot(region=(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
            text = pytesseract.image_to_string(screenshot)

            if self.target_text.get().lower() in text.lower():
                # Obtém as coordenadas aproximadas do texto
                text_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
                for i, word in enumerate(text_data["text"]):
                    if self.target_text.get().split()[0].lower() in word.lower():
                        x = self.x1 + text_data["left"][i]
                        y = self.y1 + text_data["top"][i]
                        pyautogui.moveTo(x, y)
                        self.log_message(f"Texto '{self.target_text.get()}' encontrado. Cursor movido para posição ({x}, {y}).")
                        return

                self.log_message(f"Texto '{self.target_text.get()}' não foi encontrado.")
            else:
                self.log_message(f"Texto '{self.target_text.get()}' não foi encontrado na região.")
        except Exception as e:
            self.log_message(f"Erro: {str(e)}")

# Inicializa a interface gráfica
root = tk.Tk()
app = TextSearchApp(root)
root.mainloop()

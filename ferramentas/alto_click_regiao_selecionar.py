import tkinter as tk
import pyautogui
import time
from threading import Thread

class AutomatedActions:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação de Eventos")
        self.root.geometry("600x400")
        
        # Variáveis para as regiões
        self.region_1 = None
        self.region_2 = None
        
        # Botões e interface
        self.start_button = tk.Button(root, text="Iniciar Automação", command=self.start_event, font=("Arial", 14))
        self.start_button.pack(pady=10)
        
        self.capture_button_1 = tk.Button(root, text="Definir Região 1", command=lambda: self.capture_region(1))
        self.capture_button_1.pack(pady=10)
        
        self.capture_button_2 = tk.Button(root, text="Definir Região 2", command=lambda: self.capture_region(2))
        self.capture_button_2.pack(pady=10)
        
        self.log_box = tk.Listbox(root)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def log(self, message):
        self.log_box.insert(tk.END, message)
        self.log_box.see(tk.END)
    
    def capture_region(self, region_number):
        """Abre uma janela para capturar uma região."""
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes("-fullscreen", True)
        self.selection_window.attributes("-alpha", 0.3)
        self.selection_window.config(bg='black')
        
        canvas = tk.Canvas(self.selection_window, bg="black", cursor="crosshair")
        canvas.pack(fill=tk.BOTH, expand=True)
        
        selection_start = [None]
        selection_end = [None]
        
        def on_mouse_down(event):
            selection_start[0] = (event.x, event.y)
        
        def on_mouse_drag(event):
            if selection_start[0]:
                selection_end[0] = (event.x, event.y)
                canvas.delete("selection")
                canvas.create_rectangle(
                    selection_start[0][0], selection_start[0][1], 
                    event.x, event.y, outline="red", width=2, tags="selection"
                )
        
        def on_mouse_up(event):
            if selection_start[0] and selection_end[0]:
                x1, y1 = selection_start[0]
                x2, y2 = selection_end[0]
                if region_number == 1:
                    self.region_1 = (x1, y1, x2, y2)
                    self.log(f"Região 1 definida: (x1={x1}, y1={y1}, x2={x2}, y2={y2})")
                elif region_number == 2:
                    self.region_2 = (x1, y1, x2, y2)
                    self.log(f"Região 2 definida: (x1={x1}, y1={y1}, x2={x2}, y2={y2})")
                self.selection_window.destroy()
        
        canvas.bind("<Button-1>", on_mouse_down)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_mouse_up)
    
    def execute_sequence(self):
        """Executa a sequência de ações."""
        if not self.region_1 or not self.region_2:
            self.log("Por favor, defina as regiões antes de iniciar.")
            return
        
        self.log("Iniciando automação...")
        time.sleep(5)
        
        # Clique na primeira região
        x1, y1, x2, y2 = self.region_1
        x_click = int((x1 + x2) / 2)
        y_click = int((y1 + y2) / 2)
        pyautogui.click(x_click, y_click)
        self.log(f"Clicado na Região 1 em ({x_click}, {y_click})")
        time.sleep(1)
        
        # Movimento para a segunda região
        x1, y1, x2, y2 = self.region_2
        x_move = int((x1 + x2) / 2)
        y_move = int((y1 + y2) / 2)
        pyautogui.moveTo(x_move, y_move)
        self.log(f"Movido para Região 2 em ({x_move}, {y_move})")
        time.sleep(10)
        
        # Sequência de teclas
        for _ in range(3):
            pyautogui.press('w')
        for _ in range(6):
            pyautogui.press('a')
        pyautogui.press('f')
        self.log("Automação concluída.")
    
    def start_event(self):
        """Inicia a automação em uma thread separada."""
        thread = Thread(target=self.execute_sequence)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatedActions(root)
    root.mainloop()

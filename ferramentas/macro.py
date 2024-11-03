import tkinter as tk
from tkinter import messagebox
import keyboard
import threading
import time
from pynput.keyboard import Controller as PynputController

pynput_keyboard = PynputController()

class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Macro de Sequência de Botões")
        
        self.original_sequence = []  # Sequência original para referência
        self.sequence = []  # Sequência atual usada durante a execução
        self.is_running = False
        
        # Interface para adicionar botões e intervalos
        self.button_label = tk.Label(root, text="Botão (separado por vírgulas):")
        self.button_label.pack()
        
        self.button_entry = tk.Entry(root)
        self.button_entry.pack()
        
        self.interval_label = tk.Label(root, text="Intervalo (ms):")
        self.interval_label.pack()
        
        self.interval_entry = tk.Entry(root)
        self.interval_entry.pack()
        
        self.add_button = tk.Button(root, text="Adicionar à Sequência", command=self.add_to_sequence)
        self.add_button.pack()
        
        self.start_button = tk.Button(root, text="Iniciar Macro", command=self.start_macro)
        self.start_button.pack()
        
        # Área de log para exibir as ações
        self.log_text = tk.Text(root, height=10, width=50, state='disabled')
        self.log_text.pack()

        # Configurar o listener para ativar/desativar o macro
        keyboard.add_hotkey('num 1+num 2', self.start_macro)
        keyboard.add_hotkey('num 7+num 8', self.stop_macro)

    def add_to_sequence(self):
        buttons = self.button_entry.get().split(",")  # Divide os botões em uma lista
        try:
            interval = int(self.interval_entry.get())
            for button in buttons:
                button = button.strip()  # Remove espaços extras
                self.original_sequence.append((button, interval))
            messagebox.showinfo("Adicionado", f"Sequência {', '.join(buttons)} com intervalo {interval}ms adicionada!")
            self.log(f"Sequência adicionada: {', '.join(buttons)} com intervalo {interval}ms")
        except ValueError:
            self.log("Erro: Intervalo deve ser um número inteiro.")
            messagebox.showerror("Erro", "Intervalo deve ser um número inteiro.")
        
        self.button_entry.delete(0, tk.END)
        self.interval_entry.delete(0, tk.END)

    def start_macro(self):
        if not self.original_sequence:
            self.log("Erro: Nenhuma sequência adicionada. A macro não pode ser iniciada.")
            messagebox.showerror("Erro", "Adicione ao menos uma sequência de botões.")
            return
        
        if self.is_running:
            self.log("Aviso: Macro já está em execução.")
            messagebox.showinfo("Aviso", "Macro já em execução.")
            return

        self.sequence = self.original_sequence[:]  # Restaura a sequência original
        self.is_running = True
        self.log("Macro iniciada")
        macro_thread = threading.Thread(target=self.run_macro)
        macro_thread.start()
        
    def run_macro(self):
        self.log(f"Execução da macro com {len(self.sequence)} comandos.")
        for button, interval in self.sequence:
            if not self.is_running:
                self.log("Execução da macro interrompida.")
                break
            self.log(f"Pressionando botão: {button} com intervalo de {interval}ms.")
            
            try:
                pynput_keyboard.press(button)
                pynput_keyboard.release(button)
                self.log(f"Botão '{button}' pressionado e liberado.")
            except ValueError:
                self.log(f"Erro: '{button}' não é uma tecla válida.")
            
            time.sleep(interval / 1000)
        
        self.is_running = False
        self.log("Macro finalizada")

    def stop_macro(self):
        if self.is_running:
            self.is_running = False
            self.log("Macro interrompida pelo usuário.")
            messagebox.showinfo("Parado", "A macro foi interrompida.")
        else:
            self.log("Macro já está parada.")
            messagebox.showinfo("Parado", "A macro não estava em execução.")

    def log(self, message):
        # Adiciona a mensagem de log na área de texto
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)  # Rolagem automática para o fim

# Configurações iniciais da interface e do monitor de teclado
root = tk.Tk()
app = MacroApp(root)
root.mainloop()

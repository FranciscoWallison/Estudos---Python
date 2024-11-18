import tkinter as tk
import pyautogui
import time
from threading import Thread

# Coordenadas fixas das regiões
region_1 = (1768, 170, 1826, 220)  # Primeira região
region_2 = (1408, 607, 1632, 639)  # Segunda região
region_3 = (1518, 991, 1736, 1025) 
region_4 = (1852, 46, 1884, 80)
region_5 = (1836, 363, 1869, 394)
region_6 = (1073, 490, 1135, 512)


def execute_sequence():
    """Executa a sequência de ações com base nas regiões fixas."""
    time.sleep(5)  # Aguarda 5 segundos após iniciar
    
    # Clique na primeira região
    x1, y1, x2, y2 = region_1
    x_click = (x1 + x2) // 2
    y_click = (y1 + y2) // 2
    pyautogui.click(x_click, y_click)
    print(f"Clicado na Região 1 em ({x_click}, {y_click})")
    time.sleep(1)  # Aguarda 1 segundo
    
    # Movimento para a segunda região
    x1, y1, x2, y2 = region_2
    x_move = (x1 + x2) // 2
    y_move = (y1 + y2) // 2
    pyautogui.moveTo(x_move, y_move)
    pyautogui.click(x_move, y_move)
    print(f"Movido para Região 2 em ({x_move}, {y_move})")
    time.sleep(40)  # Aguarda 10 segundos
    
    # Executa a sequência de teclas
    for _ in range(3):
        pyautogui.keyDown('w')
        time.sleep(0.1)
        pyautogui.keyUp('w')
    for _ in range(2):
        pyautogui.keyDown('a')
        time.sleep(0.1)
        pyautogui.keyUp('a')

    time.sleep(1)
    pyautogui.press('f')
    time.sleep(1)

    x1, y1, x2, y2 = region_3
    x_click = (x1 + x2) // 2
    y_click = (y1 + y2) // 2
    pyautogui.click(x_click, y_click)
    print(f"Clicado na Região 3 em ({x_click}, {y_click})")
    time.sleep(1)  # Aguarda 1 segundo

    # iniciar o novo evento de 
    x1, y1, x2, y2 = region_3
    x_click = (x1 + x2) // 2
    y_click = (y1 + y2) // 2
    pyautogui.click(x_click, y_click)
    print(f"Clicado na Região 4 que se repete na mesa da 3 em ({x_click}, {y_click})")
    time.sleep(1)  # Aguarda 1 segundo

    x1, y1, x2, y2 = region_4
    x_click = (x1 + x2) // 2
    y_click = (y1 + y2) // 2
    pyautogui.click(x_click, y_click)
    print(f"Clicado na Região 4 em ({x_click}, {y_click})")
    time.sleep(1)  # Aguarda 1 segundo

    x1, y1, x2, y2 = region_5
    x_click = (x1 + x2) // 2
    y_click = (y1 + y2) // 2
    pyautogui.click(x_click, y_click)
    print(f"Clicado na Região 5 em ({x_click}, {y_click})")
    time.sleep(1)  # Aguarda 1 segundo 

    x1, y1, x2, y2 = region_6
    x_click = (x1 + x2) // 2
    y_click = (y1 + y2) // 2
    pyautogui.click(x_click, y_click)
    print(f"Clicado na Região 6 em ({x_click}, {y_click})")
    time.sleep(1)  # Aguarda 1 segundo

    print("Automação concluída.")

def start_event():
    """Inicia a automação em uma thread separada."""
    thread = Thread(target=execute_sequence)
    thread.start()

# Interface gráfica
root = tk.Tk()
root.title("Automação de Eventos")

start_button = tk.Button(root, text="Iniciar", command=start_event, font=("Arial", 14))
start_button.pack(pady=20)

root.geometry("300x100")
root.mainloop()

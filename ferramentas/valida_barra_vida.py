import pyautogui
import numpy as np
from PIL import Image
import cv2
import tkinter as tk
from tkinter import ttk
import threading
import time

# Função para verificar se a cor é um tom de verde
def cor_verdadeiro(cor):
    hsv = cv2.cvtColor(np.uint8([[cor]]), cv2.COLOR_RGB2HSV)[0][0]

    # Definindo limites para a cor verde no espaço HSV
    verde_min = np.array([35, 50, 50])  # mínimo para verde
    verde_max = np.array([85, 255, 255])  # máximo para verde

    if np.all(verde_min <= hsv) and np.all(hsv <= verde_max):
        return True
    return False

# Função para verificar se a cor é um tom de cinza (vida vazia)
def cor_vida_vazia(cor):
    # Convertendo a cor RGB para um valor em escala de cinza
    cinza = np.mean(cor)  # A média de R, G, B é o valor de cinza
    # Se a diferença entre os canais R, G, B for pequena, é um tom de cinza
    if abs(cor[0] - cor[1]) < 10 and abs(cor[1] - cor[2]) < 10:
        return True
    return False

# Região da tela da barra de vida
regiao = (132, 82, 351, 90)

# Função para calcular a porcentagem de vida com base nas cores predominantes
def calcular_vida_percentual(imagem):
    # Converter a imagem para um array numpy
    imagem_np = np.array(imagem)

    # Reshaping para obter as cores em uma lista
    cores = imagem_np.reshape(-1, 3)

    # Contagem das cores predominantes
    verde_count = sum(1 for cor in cores if cor_verdadeiro(cor))
    vida_vazia_count = sum(1 for cor in cores if cor_vida_vazia(cor))

    # Calcular a porcentagem de vida
    total_count = len(cores)
    if total_count == 0:
        return 0  # Se não houver pixels, retornar 0

    percentual_vida = (verde_count / total_count) * 100
    return percentual_vida

# Função para capturar a imagem da região e calcular a vida
def verificar_barra_vida():
    while rodando:
        # Capturar a região da tela
        screenshot = pyautogui.screenshot(region=regiao)

        # Calcular a porcentagem de vida
        percentual_vida = calcular_vida_percentual(screenshot)

        # Atualizar a interface com a porcentagem de vida
        label_vida.config(text=f"Porcentagem de vida: {percentual_vida:.2f}%")

        # Atrasar a execução para não sobrecarregar o processamento
        time.sleep(1)

# Função para iniciar o loop de verificação em uma thread separada
def iniciar_verificacao():
    global rodando
    rodando = True
    threading.Thread(target=verificar_barra_vida, daemon=True).start()

# Função para parar o loop de verificação
def parar_verificacao():
    global rodando
    rodando = False
    label_vida.config(text="Verificação parada.")

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Verificador de Barra de Vida")

# Criando um botão para iniciar a verificação
btn_iniciar = ttk.Button(root, text="Validar", command=iniciar_verificacao)
btn_iniciar.pack(pady=10)

# Criando um botão para parar a verificação
btn_parar = ttk.Button(root, text="Parar", command=parar_verificacao)
btn_parar.pack(pady=10)

# Criando um rótulo para exibir a porcentagem de vida
label_vida = ttk.Label(root, text="Porcentagem de vida: 0.00%", font=("Arial", 14))
label_vida.pack(pady=20)

# Variável para controlar o loop
rodando = False

# Iniciar a interface
root.mainloop()

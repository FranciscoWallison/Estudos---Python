import cv2
import numpy as np
import pyautogui
import time

# Lista de templates (imagens para detectar)
templates = [
    "press_q_1.png", "press_q_2.png", "press_q_3.png", "press_q_4.png",
    "press_q_5.png", "press_q_6.png", "press_q_7.png", "captura_1.png",
    "captura_2.png", "captura_3.png", "captura_4.png",
    "captura_5.png", "captura_6.png", "captura_7.png",
]

# Coordenadas do centro da região e dimensões
x_centro, y_centro = 964, 720
largura, altura = 127, 117

# Limite de correspondência (ajuste conforme necessário)
MATCH_THRESHOLD = 0.8

# Carregar todos os templates em escala de cinza
templates_gray = [cv2.imread(template, 0) for template in templates]

# Monitorar continuamente
print("Iniciando monitoramento...")
while True:
    start_time = time.time()

    # Calcula a região dinamicamente ao redor do ponto central
    x_inicial = x_centro - largura // 2
    y_inicial = y_centro - altura // 2
    region = (x_inicial, y_inicial, largura, altura)

    # Capturar a região da tela
    screenshot = pyautogui.screenshot(region=region)
    screen_np = np.array(screenshot)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

    # Procurar cada template na captura
    for idx, template in enumerate(templates_gray):
        # Verificar tamanhos para evitar erro
        if screen_gray.shape[0] < template.shape[0] or screen_gray.shape[1] < template.shape[1]:
            print(f"Template {templates[idx]} é maior que a região capturada. Redimensionando...")
            template = cv2.resize(template, (screen_gray.shape[1], screen_gray.shape[0]))

        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # Se encontrar correspondência suficiente
        if max_val > MATCH_THRESHOLD:
            x, y = max_loc
            h, w = template.shape
            # print(f"Encontrado: {templates[idx]} na posição {x}, {y}, precisão {max_val:.2f}")
            pyautogui.press('q')
            
            # Destacar na região capturada (apenas para depuração)
            cv2.rectangle(screen_np, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break

    # Tempo gasto por iteração (ajuda a depurar desempenho)
    end_time = time.time()
    print(f"Tempo de iteração: {end_time - start_time:.4f} segundos")

    # Mostrar captura com deteções destacadas (opcional)
    cv2.imshow('Monitoramento', screen_np)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

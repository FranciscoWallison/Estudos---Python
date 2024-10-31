import cv2
import pyautogui
import numpy as np
import time
import tkinter as tk
import threading
import keyboard
import random
import os
import datetime

from pynput.keyboard import Controller as PynputController
from threading import Event, Thread

pynput_keyboard = PynputController()


class RPGMonsterDetectionBot:
    def __init__(self, monster_images_paths, additional_images_paths, log_callback, attack_duration=30*60):
        # Carrega múltiplas imagens de referência e imagens adicionais para verificação
        self.monster_templates = [cv2.imread(path, 0) for path in monster_images_paths]
        self.additional_images = [cv2.imread(path, 0) for path in additional_images_paths]
        self.running = False
        self.attack_duration = attack_duration
        self.time_left = attack_duration
        self.log_callback = log_callback

    def capture_background_screenshots(self):
        screenshot_dir = r"C:\\Users\\wallison\\Pictures\\teste\\bot"
        os.makedirs(screenshot_dir, exist_ok=True)  # Cria o diretório se não existir
        
        while self.running:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
            
            screen = pyautogui.screenshot()
            screen.save(screenshot_path)  # Salva a captura de tela
            
            self.log_event(f"Captura de tela salva em: {screenshot_path}")
            time.sleep(10)  # Pausa de 10 segundos

    def screenshot(self):
        screen = pyautogui.screenshot()
        screen = np.array(screen)
        return cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

    def match_image(self):
        screen_gray = self.screenshot()
        
        # Verifica cada template e retorna True se algum deles for encontrado
        for template in self.monster_templates:
            res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8  # Ajuste conforme necessário
            if res.max() >= threshold:  # Se a correspondência com o threshold for atingida
                self.log_event(f"Monstro encontrado com pontuação de {res.max()}")
                return True
        return False
    
    def image_in_screen(self):
        """Verifica se qualquer imagem adicional está presente na tela."""
        screen_gray = self.screenshot()
        for additional_image in self.additional_images:
            res = cv2.matchTemplate(screen_gray, additional_image, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            if res.max() >= threshold:
                self.log_event("Imagem adicional detectada.")
                return True
        return False
    
    def log_event(self, message):
        """Chama a função de log_callback para exibir mensagens na interface."""
        self.log_callback(message)

    def random_movement(self):
        directions = ['w', 'a', 's', 'd']
        diagonal_movements = [('w', 'd'), ('w', 'a'), ('s', 'd'), ('s', 'a')]
        
        # Determina uma sequência de movimentos aleatória
        num_moves = random.randint(2, 5)  # Número de movimentos a serem feitos
        for _ in range(num_moves):
            if random.random() < 0.3:  # 30% de chance de fazer um movimento diagonal
                move = random.choice(diagonal_movements)
                self.log_event(f"Movendo-se diagonalmente para: {move[0]} + {move[1]}")
                pyautogui.press(move[0])
                pyautogui.press(move[1])
            else:
                direction = random.choice(directions)
                self.log_event(f"Movendo-se para: {direction}")
                pyautogui.press(direction)

            # Pequeno intervalo entre cada movimento
            time.sleep(random.uniform(0.3, 0.7))

        self.log_event("Movimento aleatório concluído.")
        self.random_movement_2()  # Move por 5 segundos aleatoriamente


    def random_movement_2(self):
        """
        Move o personagem aleatoriamente usando as teclas 'w', 'a', 's', 'd' por um curto período.
        
        Parameters:
        - 5 (int): Duração total do movimento em segundos.
        """
        start_time = time.time()
        keys = ['w', 'a', 's', 'd']

        while time.time() - start_time < 5:
            key = random.choice(keys)
            pyautogui.keyDown(key)  # Pressiona a tecla
            time.sleep(random.uniform(0.1, 0.3))  # Espera um curto período
            pyautogui.keyUp(key)  # Solta a tecla
            time.sleep(random.uniform(0.1, 0.5))  # Intervalo entre movimentos

    def bot_movement(self):
        # Evento para controlar início e parada
        stop_event = Event()
        
        def move():
            keys = ['w', 'a', 's', 'd']
            while not stop_event.is_set():
                key = random.choice(keys)
                keyboard.press(key)
                time.sleep(0.05)  # Curto período para suavidade
                keyboard.release(key)
                time.sleep(random.uniform(0.3, 0.7))  # Intervalo aleatório para suavidade

        # Iniciar a thread de movimento
        bot_thread = Thread(target=move)
        bot_thread.start()

        # Executar por um tempo definido e depois parar
        time.sleep(10)
        stop_event.set()
        bot_thread.join()
        self.log_event("Bot parado.")


    def random_movement_3(self):
        """
        Move o personagem aleatoriamente usando as teclas 'w', 'a', 's', 'd' e diagonais
        por um curto período, integrando movimentos suaves.
        """
        directions = ['w', 'a', 's', 'd']
        diagonal_movements = [('w', 'd'), ('w', 'a'), ('s', 'd'), ('s', 'a')]
        
        start_time = time.time()
        duration = 5  # Duração total do movimento em segundos
        
        while time.time() - start_time < duration:
            # Alterna entre movimentos únicos e diagonais com suavidade
            if random.random() < 0.3:  # 30% de chance para movimentos diagonais
                move = random.choice(diagonal_movements)
                self.log_event(f"Movendo-se diagonalmente para: {move[0]} + {move[1]}")
                pyautogui.keyDown(move[0])
                pyautogui.keyDown(move[1])
                time.sleep(random.uniform(0.1, 0.3))  # Espera curta para o movimento
                pyautogui.keyUp(move[0])
                pyautogui.keyUp(move[1])
            else:
                direction = random.choice(directions)
                self.log_event(f"Movendo-se para: {direction}")
                pyautogui.keyDown(direction)
                time.sleep(random.uniform(0.1, 0.3))  # Espera curta para o movimento
                pyautogui.keyUp(direction)
            
            # Pausa entre cada movimento para suavidade
            time.sleep(random.uniform(0.1, 0.5))
        
        self.log_event("Movimento aleatório concluído.")


    def simulate_mistake(self):        
        mistake_key = str(random.randint(1, 7))

        pyautogui.press(mistake_key)
        # Se o número sorteado for 3, realiza um clique com o botão esquerdo do mouse
        if mistake_key == "3":
            self.log_event("Simulando erro: clique com o botão esquerdo do mouse.")
            pyautogui.click(button='left', clicks=2, interval=0.25)
        # Pausa aleatória para simular o erro
        time.sleep(random.uniform(0.5, 1.5))

    def detect_and_log_monster(self):
        monster_found = False
        start_time = time.time()
        
        while self.running and self.time_left > 0:
            elapsed_time = time.time() - start_time
            self.time_left = max(self.attack_duration - int(elapsed_time), 0)

            if not monster_found:
                self.log_event(f"Procurando monstro... (pressionaria 'Tab') | Tempo restante: {self.time_left // 60}m {self.time_left % 60}s")
                pyautogui.press('tab')
                monster_found = self.match_image()  # Chamando corretamente a função sem parâmetros

                if monster_found:
                    self.log_event("Monstro encontrado! Iniciando ataque...")

            if monster_found:
                if self.image_in_screen():  # Se a imagem adicional estiver presente, retorne ao modo de busca
                    self.log_event("Imagem adicional detectada. Retornando ao modo de busca...")
                    self.bot_movement()
                    monster_found = False
                    continue  # Volte para o início do loop para buscar outro monstro
        
                self.log_event(f"Atacando o monstro... (pressionaria 'E' e '1') | Tempo restante: {self.time_left // 60}m {self.time_left % 60}s")
                
                pyautogui.press('e')
                time.sleep(2)
                pyautogui.press('1')
                
                time.sleep(1)
                
                if random.choices([True, False], weights=[0.2, 0.8])[0]:
                    self.random_movement()
                else:
                    self.simulate_mistake()

                time.sleep(2)
                self.random_movement_3()
                monster_found = self.match_image()  # Verifica novamente se o monstro ainda está na tela

                if not monster_found:
                    self.log_event("Monstro eliminado ou fora de alcance. Voltando a procurar...")

            elif random.choices([True, False], weights=[0.2, 0.8])[0]:
                self.random_movement()
            elif random.choices([True, False], weights=[0.2, 0.8])[0]:
                self.simulate_mistake()

            time.sleep(1)

        if self.time_left == 0:
            self.log_event("Tempo esgotado. Parando o bot...")
            self.stop()

    def start(self):
        if not self.running:
            self.log_event("Iniciando detecção de monstro...")
            self.running = True
            self.time_left = self.attack_duration
            pyautogui.hotkey('alt', 'tab')
            self.log_event("Alternando janelas com 'Alt + Tab'...")
            threading.Thread(target=self.detect_and_log_monster, daemon=True).start()
            threading.Thread(target=self.capture_background_screenshots, daemon=True).start()

    def stop(self):
        if self.running:
            self.log_event("Parando detecção de monstro...")
            self.running = False

    def update_attack_duration(self, new_duration):
        self.attack_duration = new_duration
        self.time_left = new_duration
        self.log_event(f"Duração do ataque atualizada para {self.attack_duration // 60} minutos")

def on_key_press(bot):
    while True:
        if keyboard.is_pressed('num 1') and keyboard.is_pressed('num 2'):
            bot.start()
        elif keyboard.is_pressed('num 7') and keyboard.is_pressed('num 8'):
            bot.stop()
        time.sleep(0.1)

def create_interface(bot):
    window = tk.Tk()
    window.title("RPG Monster Detection Bot")

    start_button = tk.Button(window, text="Iniciar", command=bot.start)
    start_button.pack(pady=10)

    stop_button = tk.Button(window, text="Parar", command=bot.stop)
    stop_button.pack(pady=10)

    duration_label = tk.Label(window, text="Duração (min):")
    duration_label.pack(pady=5)
    duration_entry = tk.Entry(window)
    duration_entry.insert(0, "30")
    duration_entry.pack(pady=5)

    time_left_label = tk.Label(window, text="Tempo restante: --m --s")
    time_left_label.pack(pady=10)

    log_text = tk.Text(window, height=15, width=50)
    log_text.pack(pady=10)

    def update_duration():
        try:
            new_duration = int(duration_entry.get()) * 60
            bot.update_attack_duration(new_duration)
        except ValueError:
            bot.log_event("Por favor, insira um valor numérico válido para os minutos")

    update_button = tk.Button(window, text="Atualizar Duração", command=update_duration)
    update_button.pack(pady=10)

    def log_callback(message):
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)  # Scroll para a última mensagem

    bot.log_callback = log_callback  # Define o log_callback para o bot

    threading.Thread(target=on_key_press, args=(bot,), daemon=True).start()

    def update_time_display():
        if bot.running:
            minutes, seconds = divmod(bot.time_left, 60)
            time_left_label.config(text=f"Tempo restante: {minutes}m {seconds}s")
        window.after(1000, update_time_display)

    update_time_display()
    window.mainloop()

if __name__ == "__main__":

    monster_images_paths = [
        "path/to/monster_focused.png",
        "path/to/teste__x.png",
        "path/to/teste_2.png",
        "path/to/teste__cadiado.png",
        "path/to/teste__1.png",
    ]
    additional_images_paths = [
        "path/to/additional_image.png",
        "path/to/additional_image1.png",
        "path/to/additional_image2.png",
        "path/to/additional_image3.png",
        "path/to/additional_image4.png",
        "path/to/additional_image5.png",
        "path/to/additional_image6.png",
        "path/to/additional_image7.png",
    ]
    
    
    bot = RPGMonsterDetectionBot(monster_images_paths, additional_images_paths, log_callback=lambda x: None)
    create_interface(bot)

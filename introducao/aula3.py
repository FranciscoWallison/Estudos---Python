import random

def jogo_adivinhacao():
    jogar_novamente = 's'
    
    while jogar_novamente.lower() == 's':
        numero_secreto = random.randint(1, 10)
        acertou = False
        
        print("Estou pensando em um número entre 1 e 10. Tente adivinhar!")
        
        while not acertou:
            try:
                palpite = int(input("Digite seu palpite: "))
                
                if palpite < 1 or palpite > 10:
                    print("Por favor, insira um número entre 1 e 10.")
                    continue
                
                if palpite < numero_secreto:
                    print("Errado! O número é maior que", palpite)
                elif palpite > numero_secreto:
                    print("Errado! O número é menor que", palpite)
                else:
                    print("Parabéns! Você acertou!")
                    acertou = True
            except ValueError:
                print("Entrada inválida! Por favor, insira um número.")
        
        jogar_novamente = input("Deseja jogar novamente? (s/n): ")
    
    print("Obrigado por jogar!")

if __name__ == "__main__":
    jogo_adivinhacao()

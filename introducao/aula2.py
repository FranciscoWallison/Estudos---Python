def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Erro: Divisão por zero!"
    return x / y

def calculator():
    print("Bem-vindo à calculadora básica!")
    
    while True:
        try:
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))
        except ValueError:
            print("Por favor, insira números válidos!")
            continue

        print("Escolha a operação:")
        print("1. Adição")
        print("2. Subtração")
        print("3. Multiplicação")
        print("4. Divisão")

        choice = input("Operação escolhida: ")

        if choice == '1':
            print(f"Resultado: {num1} + {num2} = {add(num1, num2)}")
        elif choice == '2':
            print(f"Resultado: {num1} - {num2} = {subtract(num1, num2)}")
        elif choice == '3':
            print(f"Resultado: {num1} * {num2} = {multiply(num1, num2)}")
        elif choice == '4':
            print(f"Resultado: {divide(num1, num2)}")
        else:
            print("Operação inválida!")

        next_calculation = input("Deseja realizar outra operação? (s/n): ")
        if next_calculation.lower() != 's':
            break

    print("Obrigado por usar a calculadora básica!")

if __name__ == "__main__":
    calculator()

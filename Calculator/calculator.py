def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

def main():
    print("Basic Calculator")
    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    while True:
        choice = input("Enter choice (1/2/3/4): ")

        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                continue

            if choice == '1':
                print(f"The result of {num1} + {num2} is {add(num1, num2)}")
            elif choice == '2':
                print(f"The result of {num1} - {num2} is {subtract(num1, num2)}")
            elif choice == '3':
                print(f"The result of {num1} * {num2} is {multiply(num1, num2)}")
            elif choice == '4':
                print(f"The result of {num1} / {num2} is {divide(num1, num2)}")

            next_calculation = input("Do you want to perform another calculation? (yes/no): ").lower()
            if next_calculation != 'yes':
                break
        else:
            print("Invalid Input")

if __name__ == "__main__":
    main()

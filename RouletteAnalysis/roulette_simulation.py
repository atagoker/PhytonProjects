import random
from collections import Counter

numbers = list(range(37))
red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
even_numbers = set(range(2, 37, 2))
odd_numbers = set(range(1, 36, 2))

def spin_roulette(spins):
    results = Counter()
    
    for _ in range(spins):
        number = random.choice(numbers)
        
        results[number] += 1
        
        if number in red_numbers:
            results['red'] += 1
        elif number in black_numbers:
            results['black'] += 1
            
        if number in even_numbers:
            results['even'] += 1
        elif number in odd_numbers:
            results['odd'] += 1
        
        if 1 <= number <= 18:
            results['1-18'] += 1
        elif 19 <= number <= 36:
            results['19-36'] += 1
        
        if 1 <= number <= 12:
            results['1st 12'] += 1
        elif 13 <= number <= 24:
            results['2nd 12'] += 1
        elif 25 <= number <= 36:
            results['3rd 12'] += 1
            
        if number % 3 == 0:
            results['2 to 1, 3rd col'] += 1
        elif number % 3 == 1:
            results['2 to 1, 1st col'] += 1
        elif number % 3 == 2:
            results['2 to 1, 2nd col'] += 1
            
    return results

def main():
    spins = int(input("Enter the number of spins (1000, 10000, 100000, 1000000): "))
    if spins not in [1000, 10000, 100000, 1000000]:
        print("Invalid number of spins.")
        return
    
    results = spin_roulette(spins)
    
    print(f"Results after {spins} spins:")
    for key in sorted(results.keys()):
        print(f"{key}: {results[key]}")

if __name__ == "__main__":
    main()

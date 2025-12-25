import os
from analyzer import warden_scan  # analyzer.py-дан функцияны шақыру
from colorama import Fore, Style, init

# Түстерді іске қосу
from database import init_db
init_db()

def run_backend():
    # Экранды тазалау (тек эстетика үшін)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Fore.CYAN}{Style.BRIGHT}=== WARDEN-XAI BACKEND MODULE ===")
    print(f"{Fore.WHITE}Статус: Логикалық тексеріс режимі қосулы.\n")

    while True:
        # Пайдаланушыдан мәтін сұрау
        user_input = input(f"{Fore.YELLOW}Тексеруге мәтін енгізіңіз (шығу үшін 'exit' жазыңыз): ")
        
        if user_input.lower() == 'exit':
            print(f"{Fore.RED}Бағдарлама аяқталды.")
            break

        # analyzer.py-дағы функцияны қолдану
        result = warden_scan(user_input)

        # Нәтижені шығару
        print(f"\n{Fore.WHITE}--- НӘТИЖЕ ---")
        print(f"Қауіп статусы: {result['status']}")
        print(f"Қауіп пайызы: {result['score']}%")
        
        if result['alerts']:
            print(f"Себептері:")
            for alert in result['alerts']:
                print(f"{Fore.RED}- {alert}")
        else:
            print(f"{Fore.GREEN}- Ешқандай қауіп нышандары табылмады.")
        
        print(f"{Fore.WHITE}{'-'*40}\n")

if __name__ == "__main__":
    run_backend()
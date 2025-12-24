import platform
import os

print("--- Warden System Check ---")
print(f"Жүйе: {platform.system()}")
print(f"Нұсқа: {platform.release()}")
print(f"Пайдаланушы: {os.getlogin()}")
print("---------------------------")
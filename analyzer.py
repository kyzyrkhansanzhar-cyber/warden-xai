import hashlib
import os
import re
from database import save_scan_result

# --- 1. ФАЙЛДАРДЫ ТЕКСЕРУ БӨЛІМІ (File Analysis) ---
def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return None

def analyze_file(file_path):
    if not os.path.exists(file_path):
        return "Файл табылмады"
    
    file_hash = calculate_hash(file_path)
    # Әзірге қарапайым тексеріс
    status = "CLEAN" 
    
    save_scan_result(os.path.basename(file_path), file_hash, status)
    return {"status": status, "hash": file_hash}

# --- 2. МӘТІНДІ ТЕКСЕРУ БӨЛІМІ (Phishing Detection) ---
def warden_scan(text):
    keywords = [
        'ұтыс', 'утыс', 'сыйлық', 'сыйлык', 'акция', 'тегін', 'тегин', 
        'теңге', 'тенге', 'жүлде', 'жулде', 'ұттыңыз', 'уттыныз', 'утып',
        'ақша', 'акша'
    ]
    suspicious_domains = ['.tk', '.xyz', '.ga', '.cf', '.ml', 'bit.ly', 'tinyurl']
    
    alerts = []
    score = 0
    text_lower = text.lower()

    for word in keywords:
        if word in text_lower:
            alerts.append(f"Күмәнді сөз: {word}")
            score += 25

    for domain in suspicious_domains:
        if domain in text_lower:
            alerts.append(f"Күмәнді сілтеме: {domain}")
            score += 40
            break

    if any(emoji in text for emoji in ['🎁', '💰', '🚨', '💸']):
        alerts.append("Күмәнді эмодзилер табылды")
        score += 15

    score = min(score, 100)
    status = "DANGEROUS" if score >= 70 else "SUSPICIOUS" if score >= 30 else "CLEAN"

    # Базаға сақтау
    save_scan_result("TEXT_SCAN", "N/A", status)
    return {"status": status, "score": score, "alerts": alerts}
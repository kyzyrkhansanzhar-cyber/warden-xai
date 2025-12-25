import hashlib
import os
import re
import json
from database import save_scan_result

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def analyze_file(file_path):
    if not os.path.exists(file_path):
        return "Файл табылмады"
    file_hash = calculate_hash(file_path)
    status = "CLEAN" 
    save_scan_result(os.path.basename(file_path), file_hash, status, 0, "File scan performed")
    return {"status": status, "hash": file_hash}

def warden_scan(text):
    config = load_config()
    keywords = config['phishing_keywords']
    domains = config['suspicious_domains']
    
    alerts = []
    score = 0
    text_lower = text.lower()

    for word in keywords:
        if word in text_lower:
            alerts.append(f"Сөз: {word}")
            score += 25

    for domain in domains:
        if domain in text_lower:
            alerts.append(f"Домен: {domain}")
            score += 40
            break

    if any(emoji in text for emoji in ['🎁', '💰', '🚨', '💸']):
        alerts.append("Күмәнді эмодзи")
        score += 15

    score = min(score, 100)
    threshold = config['scanner_settings']['risk_threshold']
    status = "DANGEROUS" if score >= threshold else "SUSPICIOUS" if score >= 30 else "CLEAN"

    # Базаға толық ақпаратты сақтау
    save_scan_result("TEXT_SCAN", "N/A", status, score, ", ".join(alerts))
    
    return {"status": status, "score": score, "alerts": alerts}
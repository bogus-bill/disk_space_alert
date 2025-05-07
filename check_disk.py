#!/usr/bin/env python3

import shutil
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# Configuration
PARTITION = '/'  # à adapter si nécessaire
THRESHOLD = 10  # seuil d'utilisation en %
MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SENDER = os.getenv("MAIL_SENDER")
MAIL_RECEIVER = "elias.buisson@gmail.com"


def check_disk():
    total, used, free = shutil.disk_usage(PARTITION)
    used_percent = round((used / total) * 100)
    free_mb = round(free / (1024 * 1024))  # conversion en Mo

    print(f"Utilisation du disque : {used_percent}% - Espace libre : {free_mb} Mo")

    if used_percent >= THRESHOLD:
        body = (
            f"⚠️ Alerte : le disque monté sur {PARTITION} est utilisé à {used_percent}%.\n"
            f"Il reste seulement {free_mb} Mo d'espace libre.\n"
            f"Seuil d'alerte défini à {THRESHOLD}% d'utilisation.\n\n"
            "Veuillez libérer de l'espace dès que possible."
        )
        send_email(body)


def send_email(body, subject="🚨 Alerte Disque - Espace critique"):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = MAIL_SENDER
    msg["To"] = MAIL_RECEIVER

    try:
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
            server.starttls()
            server.login(MAIL_USER, MAIL_PASSWORD)
            server.sendmail(MAIL_SENDER, [MAIL_RECEIVER], msg.as_string())
            print("✅ Email envoyé avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email : {e}")


if __name__ == "__main__":
    check_disk()

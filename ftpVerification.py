import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Configuration de l'email
EMAIL_HOST = "mail.smarttech.sn"
EMAIL_PORT = 587
EMAIL_ADDRESS = "mouhamed@ucad.sn"
EMAIL_PASSWORD = "P@sser2023"
EMAIL_DESTINATION = "fatou@ucad.sn"

# Fonction pour envoyer un e-mail
def envoyer_email(fichier):
    sujet = "Nouveau fichier téléversé"
    corps = f"Un nouveau fichier a été téléversé : {fichier}"
    
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = EMAIL_DESTINATION
    message["Subject"] = sujet
    message.attach(MIMEText(corps, "plain"))
    
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as serveur:
            serveur.starttls()
            serveur.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            serveur.sendmail(EMAIL_ADDRESS, EMAIL_DESTINATION, message.as_string())
        print(f"E-mail envoyé avec succès pour le fichier {fichier}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

# Handler pour surveiller les changements dans le répertoire
class SurveilleurFTP(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Fichier détecté : {event.src_path}")
            envoyer_email(event.src_path)

# Répertoire à surveiller
dossier_surveille = "/home/ftpuser/ftp"

if __name__ == "__main__":
    event_handler = SurveilleurFTP()
    observer = Observer()
    observer.schedule(event_handler, dossier_surveille, recursive=True)
    observer.start()
    print(f"Surveillance du répertoire : {dossier_surveille}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

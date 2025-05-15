import imaplib
import email
from email.utils import parseaddr
from dotenv import load_dotenv
import os

def conect_gmail(mail, clave):
    usuario = mail
    clave = clave
    imap_url = "imap.gmail.com"
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(usuario, clave)
    return mail

def print_info(id,mensaje,adjuntos,ignorado):
    print(f"⛔ Archivo ignorado: {ignorado}")
    print(f"✅ Mail de info@diverso.ar encontrado con ID: {id.decode()}")
    print("Asunto:", mensaje["Subject"])
    print("Fecha:", mensaje["Date"])
    print("Adjuntos:", adjuntos)
    print("-" * 40)



def read_inbox (cant = 10, info_log=False):
    load_dotenv()
    mail = conect_gmail(
                        os.getenv("EMAIL_USER"),
                        os.getenv("EMAIL_PASS")
            )

    mail.select("inbox")
    status, mensajes = mail.search(None, 'FROM', '"info@diverso.ar"')
    mail_ids = mensajes[0].split()[-cant:]
    for i in mail_ids[-20:]:
        status, data = mail.fetch(i, "(RFC822)")
        mensaje = email.message_from_bytes(data[0][1])
        remitente = parseaddr(mensaje["From"])[1]
        adjuntos = []
        ignorados = []
        no_relevantes = ["datos", "whatsapp", "cbu", "presu"]

        if remitente == "info@diverso.ar":
            for parte in mensaje.walk():
                if parte.get_content_disposition() == "attachment":
                    filename = parte.get_filename().lower()
                    if any(palabra in filename for palabra in no_relevantes):
                        ignorados.append(filename)
                        continue
                    adjuntos.append(filename)
        if info_log:
            print_info(i,mensaje,adjuntos,ignorados)


    mail.logout()

read_inbox(cant=10, info_log=True)
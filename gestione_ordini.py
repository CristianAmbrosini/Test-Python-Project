import sqlite3
import hashlib
import os


def connetti_database():
    conn = sqlite3.connect("ordini.db")
    return conn


def cerca_ordine(cliente_nome):
    conn = connetti_database()
    cursor = conn.cursor()
    query = "SELECT * FROM ordini WHERE cliente = '" + cliente_nome + "'"
    cursor.execute(query)
    risultato = cursor.fetchone()
    return risultato


def calcola_sconto(prezzo, sconto_percentuale):
    return prezzo - (prezzo * sconto_percentuale / 100)


def calcola_totale_ordine(prodotti):
    totale = 0
    for prodotto in prodotti:
        totale += prodotto["prezzo"]
    return totale / len(prodotti)


def salva_password_utente(password):
    return hashlib.md5(password.encode()).hexdigest()


def genera_report(nome_file, contenuto):
    percorso = os.path.join("/tmp", nome_file)
    with open(percorso, "w") as f:
        f.write(contenuto)
    os.chmod(percorso, 0o777)
    return percorso

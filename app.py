from flask import Flask, jsonify
import requests
import schedule
import threading
import time
import os

app = Flask(__name__)

EMAIL = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")
LOGIN_URL = "https://thecircleads.com/login"

session = requests.Session()
minutos_totales = 0

def login():
    data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    res = session.post(LOGIN_URL, data=data)
    return "dashboard" in res.url

def ver_videos_simulados():
    global minutos_totales
    if login():
        minutos = 10
        minutos_totales += minutos
        print(f"Simulados {minutos} minutos. Total: {minutos_totales}")
    else:
        print("Fallo el login.")

schedule.every().day.at("07:00").do(ver_videos_simulados)

def scheduler_background():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=scheduler_background, daemon=True).start()

@app.route("/estado", methods=["GET"])
def estado():
    ganancias = minutos_totales * 0.75
    return jsonify({
        "minutos": minutos_totales,
        "ganancias_usd": round(ganancias, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

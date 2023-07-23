from flask import Flask
from threading import Thread
import datetime

app = Flask('')


@app.route('/')
def main():
    print(datetime.datetime.now().strftime("%X"))
    return "server online!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()
    print(datetime.datetime.now().strftime("%X"))

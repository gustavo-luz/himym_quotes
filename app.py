from os import environ
import flask
from flask import Flask
import tweet_bot

app = Flask(__name__)

@app.route("/generate")
def home():
    tweet_bot.main()
    return "Tweeting a HIMYM Quote..."

@app.route("/")
def message():
    
    return "Go away, you shold not GENERATE quotes stranger..."

app.run(host= '0.0.0.0', port=environ.get('PORT'))
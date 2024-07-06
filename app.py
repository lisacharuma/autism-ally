from flask import Flask, render_template

app=flask(__app__)

@app.route('/')
def hello():
    return ("Hello World!")
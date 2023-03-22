from flask import Flask
import fetch_deprem
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/deprem', methods = ['GET'])
def hello():
    DATA_SOURCE="http://www.koeri.boun.edu.tr/scripts/lst9.asp"
    data = fetch_deprem.fetch_earthquake_data(DATA_SOURCE)
    df = fetch_deprem.text_cleanup(text=data)

   

    return df

import changeDetector
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/changes", methods=['POST'])
def changes():
    old_url = request.form['old_url']
    new_url = request.form['new_url']
    resultado = changeDetector.change_detector(old_url, new_url, 'diferencia'.upper())
    return render_template('resultados.html', resultado = resultado)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == "__main__":
    app.run(debug=True)

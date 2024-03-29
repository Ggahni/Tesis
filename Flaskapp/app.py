import changeDetector
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Duración de imágenes en caché = 0

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/changes", methods=['POST'])
def changes():
    old_url = request.form['old_url']
    new_url = request.form['new_url']
    changeDetector.change_detector(old_url, new_url, 'diferencia'.upper())
    return render_template('resultados.html')

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
    app.run(debug=True)

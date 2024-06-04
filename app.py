#need clear upload before start

from flask import Flask, request, render_template, redirect, url_for, flash
from collections import Counter
import os
import string

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'


# Маршрут для отображения формы загрузки файла
@app.route('/')
def index():
    return render_template('index.html')


# Маршрут для обработки загруженного файла
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        text = text.translate(str.maketrans('', '', string.punctuation)).lower() # < for text normal

        words = text.split()
        word_counts = Counter(words)
        most_common = word_counts.most_common(5)
        return render_template('result.html', words=most_common)


if __name__ == '__main__':
    app.run(debug=True)

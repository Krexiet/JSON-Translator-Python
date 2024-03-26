from flask import Flask, render_template, request, jsonify, send_file
from translate import translate_json_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_file = request.files['input_file']
    source_language = request.form['source_language']
    target_language = request.form['target_language']
    exclude_strings = request.form.getlist('exclude_strings')

    input_filename = 'input.json'
    input_file.save(input_filename)

    output_file = 'output.json'
    translate_json_file(input_filename, output_file, target_language=target_language, exclude_strings=exclude_strings, source_language=source_language)

    # Отправляем переведенный файл клиенту
    response = send_file(output_file, as_attachment=True)
    
    # Удаляем файл после скачивания
    os.remove(output_file)
    os.remove(input_filename)

    return response

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    if 'file1' not in request.files or 'file2' not in request.files:
        return 'Nenhum arquivo enviado!'
    
    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return 'Nome de arquivo inválido!'
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename))
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename))
    file1.save(file1_path)
    file2.save(file2_path)
    
    imagem1 = Image.open(file1_path)
    imagem2 = Image.open(file2_path)
    
    if imagem1.size != imagem2.size:
        tamanho = (585, 559)
        imagem1 = imagem1.resize(tamanho)
        imagem2 = imagem2.resize(tamanho)
    
    imagem1.paste(imagem2, (0, 0), imagem2)
    
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resultado.png')
    imagem1.save(output_path)
    
    return redirect(url_for('download'))

@app.route('/download')
def download():
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], 'resultado.png'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

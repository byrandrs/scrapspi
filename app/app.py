import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials, db
import firebase_admin.messaging as messaging
from firebase_admin import messaging
from flask_socketio import SocketIO, send
from flask_cors import CORS
import pytesseract
from PIL import Image
import base64
import io

# Ruta completa al ejecutable de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# Inicializa Firebase
cred = credentials.Certificate("./scrap-rnt-firebase-adminsdk-nk1d2-ed283c15cd.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://scrap-rnt-default-rtdb.firebaseio.com/'})

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Agrega una secret key única y segura aquí. Puede ser cualquier cadena alfanumérica.
app.secret_key = 'my_secret_key'

# Configura Socket.IO
socketio = SocketIO(app)

@app.route('/firebase-messaging-sw.js')
def serve_sw():
    return send_from_directory('./', 'firebase-messaging-sw.js')


@app.route('/', methods=['GET', 'POST'])
def index():
    # Cargar la lista desde la base de datos de Firebase
    lista_ref = db.reference('resultados')
    lista = lista_ref.get()
    
    # Si lista es None, asignar un diccionario vacío
    lista = lista or {}
    
    return render_template('index.html', lista=lista)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        # Verificar que se haya enviado un archivo de imagen
        if 'file' not in request.files:
            return jsonify({'error': 'No se ha enviado ninguna imagen'}), 400

        file = request.files['file']

        # Verificar que se haya seleccionado un archivo
        if file.filename == '':
            return jsonify({'error': 'No se ha seleccionado un archivo'}), 400

        # Verificar que el archivo sea una imagen válida
        allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
        if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'Formato de imagen no válido'}), 400

        # Procesar la imagen usando pytesseract
        img = Image.open(file)
        text = pytesseract.image_to_string(img)

        # Codificar la imagen en base64 para mostrarla en la página
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Guardar el texto extraído y la imagen en Firebase
        data = {
            'text': text,
            'image': img_base64
        }
        db.reference('resultados').push(data)

        # Devolver el texto extraído como respuesta
        return jsonify({'text': text, 'image': img_base64})

    except Exception as e:
        return jsonify({'error': 'Ha ocurrido un error al procesar la imagen', 'details': str(e)}), 500
    
@app.route('/editar/<string:key>', methods=['GET', 'POST'])
def editar_elemento(key):
    lista_ref = db.reference('resultados')
    lista = lista_ref.get()

    if request.method == 'POST':
        nuevo_valor = request.form['nuevo_valor']

        # Verificar si se ha subido una nueva imagen
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                lista_ref.child(key).update({'image': get_base64_encoded_image(filename)})

        lista_ref.child(key).update({'text': nuevo_valor})
        flash(f'Elemento "{key}" actualizado correctamente')
        return redirect(url_for('index'))

    return render_template('editar_elemento.html', key=key, valor=lista[key]['text'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_base64_encoded_image(image_path):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], image_path), 'rb') as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded_string

@app.route('/eliminar/<string:key>', methods=['POST'])
def eliminar_elemento(key):
    lista_ref = db.reference('resultados')
    lista_ref.child(key).delete()
    return jsonify({'mensaje': f'Elemento "{key}" eliminado correctamente'})

@app.route('/receive_notification', methods=['POST'])
def receive_notification():
    data = request.json
    key = data['key']
    text = data['text']
    image = data['image']
    socketio.emit('new_element_added', {
        'key': key,
        'text': text,
        'image': image
    })
    return jsonify({'message': 'Notification received successfully'})



if __name__ == '__main__':
    socketio.run(app, debug=True)  # Agregamos la llamada a socketio.run para que utilice Socket.IO
    
    app.run(debug=True)

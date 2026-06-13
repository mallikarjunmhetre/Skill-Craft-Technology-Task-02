import os
import json
import time
import hashlib
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_session import Session
from werkzeug.utils import secure_filename
from encryption import (
    xor_encrypt, xor_decrypt,
    pixel_swap_encrypt, pixel_swap_decrypt,
    math_operation_encrypt, math_operation_decrypt,
    channel_shift_encrypt, channel_shift_decrypt,
    arnold_cat_map_encrypt, arnold_cat_map_decrypt,
    get_image_metadata
)
import uuid
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}
HISTORY_FILE = 'history.json'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []
def save_history(entry):
    history = load_history()
    history.insert(0, entry)
    history = history[:50]  # Keep last 50 entries
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/encrypt')
def encrypt_page():
    return render_template('encrypt.html')
@app.route('/decrypt')
def decrypt_page():
    return render_template('decrypt.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/history')
def history():
    history_data = load_history()
    return render_template('history.html', history=history_data)
@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Use PNG, JPG, JPEG, BMP'}), 400
    method = request.form.get('method', 'xor')
    key = request.form.get('key', '42')
    try:
        key_int = int(key) % 256
    except ValueError:
        key_hash = hashlib.md5(key.encode()).hexdigest()
        key_int = int(key_hash[:2], 16)
    uid = str(uuid.uuid4())[:8]
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uid}_input.png')
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{uid}_encrypted.png')
    file.save(input_path)
    try:
        metadata = get_image_metadata(input_path)
        if method == 'xor':
            xor_encrypt(input_path, output_path, key_int)
        elif method == 'pixel_swap':
            pixel_swap_encrypt(input_path, output_path, key_int)
        elif method == 'math_op':
            operation = request.form.get('operation', 'add')
            math_operation_encrypt(input_path, output_path, key_int, operation)
        elif method == 'channel_shift':
            channel_shift_encrypt(input_path, output_path, key_int)
        elif method == 'arnold_cat':
            iterations = int(request.form.get('iterations', '5'))
            arnold_cat_map_encrypt(input_path, output_path, iterations)
        else:
            return jsonify({'error': 'Invalid encryption method'}), 400
        entry = {
            'id': uid,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'operation': 'encrypt',
            'method': method,
            'filename': filename,
            'key': key_int,
            'width': metadata['width'],
            'height': metadata['height'],
            'mode': metadata['mode'],
            'output_file': f'{uid}_encrypted.png'
        }
        save_history(entry)
        return jsonify({
            'success': True,
            'uid': uid,
            'output_file': f'{uid}_encrypted.png',
            'metadata': metadata,
            'method': method,
            'key': key_int
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    method = request.form.get('method', 'xor')
    key = request.form.get('key', '42')
    try:
        key_int = int(key) % 256
    except ValueError:
        key_hash = hashlib.md5(key.encode()).hexdigest()
        key_int = int(key_hash[:2], 16)
    uid = str(uuid.uuid4())[:8]
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{uid}_enc_input.png')
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{uid}_decrypted.png')
    file.save(input_path)
    try:
        metadata = get_image_metadata(input_path)
        if method == 'xor':
            xor_decrypt(input_path, output_path, key_int)
        elif method == 'pixel_swap':
            pixel_swap_decrypt(input_path, output_path, key_int)
        elif method == 'math_op':
            operation = request.form.get('operation', 'add')
            math_operation_decrypt(input_path, output_path, key_int, operation)
        elif method == 'channel_shift':
            channel_shift_decrypt(input_path, output_path, key_int)
        elif method == 'arnold_cat':
            iterations = int(request.form.get('iterations', '5'))
            arnold_cat_map_decrypt(input_path, output_path, iterations)
        else:
            return jsonify({'error': 'Invalid decryption method'}), 400
        entry = {
            'id': uid,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'operation': 'decrypt',
            'method': method,
            'filename': filename,
            'key': key_int,
            'width': metadata['width'],
            'height': metadata['height'],
            'mode': metadata['mode'],
            'output_file': f'{uid}_decrypted.png'
        }
        save_history(entry)
        return jsonify({
            'success': True,
            'uid': uid,
            'output_file': f'{uid}_decrypted.png',
            'metadata': metadata,
            'method': method,
            'key': key_int
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/download/<filename>')
def download_file(filename):
    safe_name = secure_filename(filename)
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], safe_name)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_file(file_path, as_attachment=True, download_name=safe_name)
@app.route('/api/preview/<filename>')
def preview_file(filename):
    safe_name = secure_filename(filename)
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], safe_name)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_file(file_path, mimetype='image/png')
@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    with open(HISTORY_FILE, 'w') as f:
        json.dump([], f)
    return jsonify({'success': True})
if __name__ == '__main__':
    app.run(debug=True, port=5000)

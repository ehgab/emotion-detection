"""
Serveur Flask pour l'analyse des émotions.
Ce module fournit une API REST pour l'analyse de sentiments.
"""

import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from EmotionDetection import emotion_detector

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
CORS(app, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.before_request
def before_request():
    """Middleware exécuté avant chaque requête."""
    # Headers gérés dans after_request


@app.after_request
def add_headers(response):
    """Ajouter des headers CORS et de sécurité."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def index():
    """Route principale - sert le template index.html."""
    try:
        return render_template('index.html')
    except Exception:  # pylint: disable=broad-exception-caught
        return "<html><body><h1>Erreur de template</h1></body></html>"


@app.route('/emotionDetector', methods=['GET', 'OPTIONS', 'POST'])
def emotion_detector_endpoint():
    """Endpoint pour l'analyse des émotions."""
    if request.method == 'OPTIONS':
        return '', 200

    text_to_analyze = request.args.get('textToAnalyze', '')

    if not text_to_analyze or text_to_analyze.strip() == "":
        return jsonify({
            "message": "Texte invalide ! Veuillez réessayer !"
        }), 400

    result = emotion_detector(text_to_analyze)

    if result['dominant_emotion'] is None:
        return jsonify({
            "message": "Texte invalide ! Veuillez réessayer !"
        }), 400

    response_text = (
        f"Pour l'énoncé donné, la réponse du système est "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} "
        f"et 'sadness': {result['sadness']}. "
        f"L'émotion dominante est {result['dominant_emotion']}."
    )

    return jsonify({
        "response": response_text
    })


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Servir les fichiers statiques."""
    return send_from_directory('static', filename)


@app.route('/health')
def health():
    """Route de santé."""
    return jsonify({"status": "healthy", "service": "emotion-detection"})


@app.route('/debug')
def debug():
    """Route de debug."""
    return jsonify({
        "cwd": os.getcwd(),
        "files": os.listdir('.'),
        "templates_exists": os.path.exists('templates'),
        "index_exists": os.path.exists('templates/index.html'),
        "python_version": os.sys.version
    })


def print_startup_message():
    """Affiche le message de démarrage."""
    print("=" * 70)
    print("🚀 SERVEUR FLASK POUR IBM SKILLS NETWORK LABS")
    print("=" * 70)
    print("\n📁 Répertoire courant:", os.getcwd())
    print("📁 Contenu du dossier:")
    for item in os.listdir('.'):
        print("   -", item)
    print("\n✅ Templates disponible:", os.path.exists('templates'))
    if os.path.exists('templates'):
        print("✅ Fichiers templates:", os.listdir('templates'))
    print("\n🌐 URLs d'accès:")
    print("1. http://localhost:5000/")
    print("2. http://localhost:5000/emotionDetector?textToAnalyze=Je pense que je m'amuse")
    print("3. http://localhost:5000/debug")
    print("4. http://localhost:5000/health")
    print("\n🔧 Configuration:")
    print("   Port: 5000")
    print("   Host: 0.0.0.0")
    print("   Debug: True")
    print("\n⚠️  Si vous voyez '403 Forbidden':")
    print("   - Essayez avec curl: curl http://localhost:5000/")
    print("   - Vérifiez le panneau 'Ports' dans IBM Labs")
    print("=" * 70)


if __name__ == '__main__':
    print_startup_message()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True,
        use_reloader=False
    )
    
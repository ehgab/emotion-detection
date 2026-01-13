from flask import Flask, render_template, request, jsonify, send_from_directory
from EmotionDetection import emotion_detector
import os

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Désactiver certaines sécurités pour IBM Labs
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Middleware pour permettre l'accès
@app.before_request
def before_request():
    """Ajouter des headers pour permettre l'accès"""
    pass  # On va gérer les headers dans after_request

@app.after_request
def add_headers(response):
    """Ajouter des headers CORS et de sécurité"""
    # Headers pour permettre l'accès depuis n'importe où (en développement)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    """Route principale - sert le template index.html"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <html>
        <body>
            <h1>Erreur de template</h1>
            <p>{str(e)}</p>
            <p>Vérifiez que templates/index.html existe</p>
        </body>
        </html>
        """

@app.route('/emotionDetector', methods=['GET', 'OPTIONS'])
def emotion_detector_endpoint():
    """
    Endpoint pour l'analyse des émotions
    Format: /emotionDetector?textToAnalyze=texte
    """
    if request.method == 'OPTIONS':
        # Gérer les pré-requêtes CORS
        return '', 200
    
    text_to_analyze = request.args.get('textToAnalyze', '')
    
    if not text_to_analyze:
        return jsonify({
            "error": "Texte manquant",
            "message": "Veuillez fournir un texte à analyser dans le paramètre 'textToAnalyze'"
        }), 400
    
    result = emotion_detector(text_to_analyze)
    
    if result['dominant_emotion'] is None:
        return jsonify({
            "error": "Analyse impossible",
            "message": "Impossible d'analyser les émotions dans ce texte"
        }), 400
    
    # Format de réponse demandé
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
        "response": response_text,
        "scores": result
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Servir les fichiers statiques"""
    return send_from_directory('static', filename)

@app.route('/health')
def health():
    """Route de santé"""
    return jsonify({"status": "healthy", "service": "emotion-detection"})

@app.route('/debug')
def debug():
    """Route de debug pour vérifier l'environnement"""
    return jsonify({
        "cwd": os.getcwd(),
        "files": os.listdir('.'),
        "templates_exists": os.path.exists('templates'),
        "index_exists": os.path.exists('templates/index.html'),
        "python_version": os.sys.version
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 SERVEUR FLASK POUR IBM SKILLS NETWORK LABS")
    print("=" * 70)
    
    # Vérifier l'environnement
    print(f"\n📁 Répertoire courant: {os.getcwd()}")
    print(f"📁 Contenu du dossier:")
    for item in os.listdir('.'):
        print(f"   - {item}")
    
    print(f"\n✅ Templates disponible: {os.path.exists('templates')}")
    if os.path.exists('templates'):
        print(f"✅ Fichiers templates: {os.listdir('templates')}")
    
    print(f"\n🌐 URLs d'accès:")
    print(f"1. http://localhost:5000/")
    print(f"2. http://localhost:5000/emotionDetector?textToAnalyze=Je pense que je m'amuse")
    print(f"3. http://localhost:5000/debug (pour vérifier)")
    print(f"4. http://localhost:5000/health")
    
    print(f"\n🔧 Configuration:")
    print(f"   Port: 5000")
    print(f"   Host: 0.0.0.0 (accepte toutes les connexions)")
    print(f"   Debug: True")
    
    print(f"\n⚠️  Si vous voyez '403 Forbidden':")
    print(f"   - Essayez avec curl: curl http://localhost:5000/")
    print(f"   - Vérifiez le panneau 'Ports' dans IBM Labs")
    print(f"   - Cliquez sur l'icône 🌐 à côté du port 5000")
    
    print("=" * 70)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True,
        use_reloader=False
    )
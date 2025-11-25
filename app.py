from flask import Flask, request, jsonify, render_template_string
import anthropic
import os

app = Flask(__name__)

# Template HTML minimalista
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD Flask + IA</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .version {
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
            font-size: 12px;
            margin-bottom: 20px;
        }
        .chat-container {
            margin-bottom: 20px;
        }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            resize: vertical;
            font-family: inherit;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            width: 100%;
            margin-top: 15px;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .response {
            margin-top: 20px;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 10px;
            display: none;
        }
        .response.show {
            display: block;
        }
        .response h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .response p {
            color: #333;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        .loading {
            text-align: center;
            color: #667eea;
            display: none;
        }
        .loading.show {
            display: block;
        }
        .status {
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .status.healthy {
            background: #d4edda;
            color: #155724;
        }
        .info {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        .info p {
            color: #333;
            margin: 5px 0;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 CI/CD Flask + IA</h1>
        <div class="subtitle">Proyecto de Integración y Entrega Continua</div>
        <div style="text-align: center;">
            <span class="version">v1.0.5</span>
        </div>
        
        <div class="status healthy">
            ✅ Sistema Operativo - Pipeline CI/CD Activo
        </div>

        <div class="info">
            <p><strong>📦 Imagen:</strong> ghcr.io/DavidVMuela/muela:1.0.5</p>
            <p><strong>🌐 Despliegue:</strong> Automático via GitHub Actions</p>
            <p><strong>🤖 IA:</strong> Claude API Integration</p>
        </div>

        <div class="chat-container">
            <label for="prompt"><strong>Consulta a la IA:</strong></label>
            <textarea id="prompt" rows="4" placeholder="Escribe tu pregunta aquí...">¿Qué es CI/CD y por qué es importante?</textarea>
            <button onclick="sendRequest()">Enviar Consulta</button>
        </div>

        <div class="loading" id="loading">⏳ Procesando consulta...</div>
        
        <div class="response" id="response">
            <h3>Respuesta:</h3>
            <p id="responseText"></p>
        </div>
    </div>

    <script>
        async function sendRequest() {
            const prompt = document.getElementById('prompt').value;
            const button = document.querySelector('button');
            const loading = document.getElementById('loading');
            const response = document.getElementById('response');
            const responseText = document.getElementById('responseText');

            if (!prompt.trim()) {
                alert('Por favor, escribe una pregunta');
                return;
            }

            button.disabled = true;
            loading.classList.add('show');
            response.classList.remove('show');

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt: prompt })
                });

                const data = await res.json();
                
                if (data.response) {
                    responseText.textContent = data.response;
                    response.classList.add('show');
                } else {
                    responseText.textContent = 'Error: ' + (data.error || 'No se recibió respuesta');
                    response.classList.add('show');
                }
            } catch (error) {
                responseText.textContent = 'Error de conexión: ' + error.message;
                response.classList.add('show');
            } finally {
                button.disabled = false;
                loading.classList.remove('show');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "version": "1.0.5",
        "service": "flask-ai-cicd"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Verificar si existe API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return jsonify({
                "response": "⚠️ Modo Demo: La API key de Anthropic no está configurada. En producción, aquí se procesaría tu consulta con IA.\n\nTu pregunta fue: " + prompt
            })
        
        # Llamar a la API de Claude
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        return jsonify({"response": response_text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
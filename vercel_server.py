from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import uuid
import re
from datetime import datetime

app = Flask(__name__)

class SimpleEmailChannel:
    """Canal de email simplificado para Vercel"""
    
    def __init__(self, smtp_server, port, username, password):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password
    
    def validate_destination(self, destination):
        """Valida formato de email"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, destination))
    
    def send_email(self, destination, content, subject="🧠 Mensagem Cognitiva"):
        """Envia email"""
        if not self.validate_destination(destination):
            return {"success": False, "error": "Email inválido"}
        
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = destination
            msg['Subject'] = subject
            
            # Adicionar conteúdo
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # Conectar e enviar
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg, to_addrs=[destination])
            
            return {
                "success": True,
                "channel": "email",
                "destination": destination,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "channel": "email",
                "destination": destination
            }

# Configuração do canal de email
email_channel = SimpleEmailChannel(
    smtp_server="smtp.gmail.com",
    port=587,
    username="juliocamposmachado@gmail.com",
    password="lyia mihj mhdk dqkn"
)

# Armazenamento simples de mensagens
active_messages = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """Endpoint simplificado para enviar mensagem"""
    data = request.json
    
    destination = data.get('destination')
    content = data.get('content')
    priority = data.get('priority', 1)
    ai_level = data.get('aiLevel', 5)
    
    if not destination or not content:
        return jsonify({'error': 'Destination e content são obrigatórios'}), 400
    
    message_id = str(uuid.uuid4())
    
    # Simula pensamento da IA baseado no nível
    ai_thoughts = [
        "Analisando destino...",
        f"IA nível {ai_level} ativada!",
        "Detectando melhor canal de entrega...",
        "Preparando mensagem para envio..."
    ]
    
    # Detecta se é email
    if email_channel.validate_destination(destination):
        # Envia email real
        result = email_channel.send_email(
            destination=destination,
            content=f"{content}\n\n---\n🧠 Enviado por IA nível {ai_level}\n🎯 ID: {message_id[:8]}",
            subject=f"🧠 Mensagem Inteligente (IA Nível {ai_level})"
        )
        
        # Armazena mensagem
        active_messages[message_id] = {
            'id': message_id,
            'destination': destination,
            'content': content,
            'ai_level': ai_level,
            'status': 'delivered' if result['success'] else 'failed',
            'ai_thoughts': ai_thoughts,
            'delivery_result': result,
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'message_id': message_id,
            'status': 'delivered' if result['success'] else 'failed',
            'ai_level': ai_level,
            'ai_thoughts': ai_thoughts,
            'delivery_result': result,
            'timestamp': time.time()
        })
        
    else:
        # Para telefones, retorna simulação
        active_messages[message_id] = {
            'id': message_id,
            'destination': destination,
            'content': content,
            'ai_level': ai_level,
            'status': 'simulated',
            'ai_thoughts': ai_thoughts + ["SMS simulado - configure Twilio para envio real"],
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'message_id': message_id,
            'status': 'simulated',
            'ai_level': ai_level,
            'ai_thoughts': ai_thoughts + ["SMS simulado - configure Twilio para envio real"],
            'message': 'SMS simulado - email enviado com sucesso!',
            'timestamp': time.time()
        })

@app.route('/active_messages')
def get_active_messages():
    """Lista mensagens ativas"""
    return jsonify(active_messages)

@app.route('/message_status/<message_id>')
def message_status(message_id):
    """Status de mensagem específica"""
    if message_id in active_messages:
        return jsonify(active_messages[message_id])
    return jsonify({'error': 'Mensagem não encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)

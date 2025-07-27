from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import asyncio
import threading
import time
import json
import uuid
from datetime import datetime
from adaptive_messenger import AdaptiveMessenger, Message
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cognitive_messages_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

class CognitiveMessageServer:
    def __init__(self):
        self.active_messages = {}  # Mensagens em trânsito
        self.messenger = AdaptiveMessenger("SERVER_NODE")
        self.delivery_confirmations = {}
        
        # Inicia o messenger em thread separada
        self.messenger_thread = None
        self.start_messenger()
    
    def start_messenger(self):
        """Inicia o sistema de mensagens em thread separada"""
        def run_messenger():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.messenger.start())
        
        self.messenger_thread = threading.Thread(target=run_messenger, daemon=True)
        self.messenger_thread.start()
    
    def create_cognitive_message(self, destination, content, priority=1):
        """Cria uma mensagem cognitiva com capsulamento completo"""
        message_id = str(uuid.uuid4())
        
        # Cria mensagem cognitiva
        cognitive_message = Message(
            id=message_id,
            source="WEB_SERVER",
            destination=destination,
            content=content,
            timestamp=time.time(),
            priority=priority,
            cognizant=True,  # Sempre cognitiva
            path=["WEB_SERVER"]
        )
        
        # Capsulamento: mensagem fica no servidor até entrega
        self.active_messages[message_id] = {
            'message': cognitive_message,
            'status': 'pending',
            'created_at': datetime.now(),
            'attempts': 0,
            'last_attempt': None,
            'delivery_confirmed': False
        }
        
        # Adiciona à fila do messenger
        self.messenger.message_queue.append(cognitive_message)
        
        return message_id, cognitive_message
    
    def confirm_delivery(self, message_id):
        """Confirma entrega e remove mensagem do servidor"""
        if message_id in self.active_messages:
            self.active_messages[message_id]['delivery_confirmed'] = True
            self.active_messages[message_id]['status'] = 'delivered'
            
            # Emite confirmação via WebSocket
            socketio.emit('message_delivered', {
                'message_id': message_id,
                'timestamp': time.time()
            })
            
            # Remove do servidor após breve delay
            def cleanup():
                time.sleep(5)  # Aguarda 5 segundos
                if message_id in self.active_messages:
                    del self.active_messages[message_id]
                    print(f"🗑️ Mensagem {message_id[:8]} removida do servidor após entrega")
            
            threading.Thread(target=cleanup, daemon=True).start()
            return True
        return False
    
    def get_message_status(self, message_id):
        """Retorna status detalhado da mensagem"""
        if message_id in self.active_messages:
            msg_data = self.active_messages[message_id]
            return {
                'id': message_id,
                'status': msg_data['status'],
                'created_at': msg_data['created_at'].isoformat(),
                'attempts': msg_data['attempts'],
                'delivery_confirmed': msg_data['delivery_confirmed'],
                'learning_data': msg_data['message'].learning_data,
                'path': msg_data['message'].path,
                'clone_count': msg_data['message'].clone_count
            }
        return None
    
    def get_all_active_messages(self):
        """Retorna todas as mensagens ativas"""
        return {
            msg_id: self.get_message_status(msg_id) 
            for msg_id in self.active_messages.keys()
        }

# Instância global do servidor
cognitive_server = CognitiveMessageServer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """Endpoint para enviar mensagem cognitiva"""
    data = request.json
    
    destination = data.get('destination')
    content = data.get('content')
    priority = data.get('priority', 1)
    
    if not destination or not content:
        return jsonify({'error': 'Destination e content são obrigatórios'}), 400
    
    message_id, message = cognitive_server.create_cognitive_message(
        destination, content, priority
    )
    
    return jsonify({
        'message_id': message_id,
        'status': 'sent',
        'timestamp': time.time(),
        'message': {
            'destination': destination,
            'content': content,
            'cognitive': True
        }
    })

@app.route('/message_status/<message_id>')
def message_status(message_id):
    """Retorna status de uma mensagem específica"""
    status = cognitive_server.get_message_status(message_id)
    if status:
        return jsonify(status)
    return jsonify({'error': 'Mensagem não encontrada'}), 404

@app.route('/active_messages')
def active_messages():
    """Lista todas as mensagens ativas"""
    return jsonify(cognitive_server.get_all_active_messages())

@app.route('/confirm_delivery/<message_id>', methods=['POST'])
def confirm_delivery(message_id):
    """Confirma entrega da mensagem"""
    success = cognitive_server.confirm_delivery(message_id)
    if success:
        return jsonify({'message': 'Entrega confirmada', 'message_id': message_id})
    return jsonify({'error': 'Mensagem não encontrada'}), 404

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado ao WebSocket')
    emit('connected', {'message': 'Conectado ao Servidor de Mensagens Cognitivas'})

@socketio.on('request_status_update')
def handle_status_request(data):
    """Envia atualizações de status em tempo real"""
    message_id = data.get('message_id')
    if message_id:
        status = cognitive_server.get_message_status(message_id)
        emit('status_update', status)

# Função para monitorar mensagens e atualizar status
def monitor_messages():
    """Monitor que verifica status das mensagens periodicamente"""
    while True:
        try:
            for message_id, msg_data in list(cognitive_server.active_messages.items()):
                message = msg_data['message']
                
                # Verifica se mensagem foi entregue
                if message.destination in message.deliveries and not msg_data['delivery_confirmed']:
                    cognitive_server.confirm_delivery(message_id)
                
                # Atualiza tentativas
                msg_data['attempts'] = len(message.learning_data['successful_routes']) + len(message.learning_data['failed_routes'])
                msg_data['last_attempt'] = time.time()
                
                # Emite atualização via WebSocket
                socketio.emit('message_update', {
                    'message_id': message_id,
                    'status': cognitive_server.get_message_status(message_id)
                })
            
            time.sleep(2)  # Verifica a cada 2 segundos
        except Exception as e:
            print(f"Erro no monitor: {e}")
            time.sleep(5)

# Inicia monitor em thread separada
monitor_thread = threading.Thread(target=monitor_messages, daemon=True)
monitor_thread.start()

if __name__ == '__main__':
    print("🌐 Iniciando Servidor Web de Mensagens Cognitivas")
    print("📡 Servidor nunca perde mensagens até confirmação de entrega")
    print("🧠 Mensagens com cognição completa e aprendizado")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

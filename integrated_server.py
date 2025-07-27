from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import asyncio
import threading
import time
import json
import uuid
from datetime import datetime
from intelligent_message import ThinkingMessage
from delivery_channels import DeliveryManager, EmailChannel, SMSChannel
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cognitive_ai_messages_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

class IntelligentMessageServer:
    def __init__(self):
        self.active_messages = {}  # Mensagens ativas com IA
        self.delivery_manager = self.setup_delivery_channels()
        print("🧠 Servidor de Mensagens Inteligentes iniciado!")
    
    def setup_delivery_channels(self):
        """Configura canais de entrega reais"""
        manager = DeliveryManager()
        
        # Configuração de email (usando credenciais do usuário)
        email_channel = EmailChannel(
            smtp_server="smtp.gmail.com",
            port=587,
            username="juliocamposmachado@gmail.com",
            password="lyia mihj mhdk dqkn"  # Senha de app configurada
        )
        manager.register_channel("email", email_channel)
        
        # SMS pode ser configurado aqui quando necessário
        # sms_channel = SMSChannel(
        #     api_key="sua_api_key",
        #     api_url="https://api.twilio.com/...",
        #     sender_id="+1234567890"
        # )
        # manager.register_channel("sms", sms_channel)
        
        return manager
    
    async def create_intelligent_message(self, destination, content, priority=1, ai_level=5):
        """Cria uma mensagem inteligente com IA empacotada"""
        
        message_id = str(uuid.uuid4())
        
        # Cria mensagem com IA empacotada
        thinking_message = ThinkingMessage(
            id=message_id,
            content=content,
            destination=destination,
            source="WEB_SERVER",
            timestamp=time.time(),
            intelligence_level=ai_level
        )
        
        # Armazena no servidor
        self.active_messages[message_id] = {
            'ai_message': thinking_message,
            'status': 'thinking',
            'created_at': datetime.now(),
            'delivery_attempts': 0,
            'real_delivery_result': None
        }
        
        # Emite log inicial
        self.emit_log(f"🧠 Mensagem inteligente criada com IA nível {ai_level}")
        self.emit_log(f"🎯 Destino: {destination}")
        self.emit_log(f"💬 Conteúdo: {content}")
        
        return message_id, thinking_message
    
    async def process_intelligent_message(self, message_id):
        """Processa a mensagem com IA e entrega real"""
        
        if message_id not in self.active_messages:
            return
        
        msg_data = self.active_messages[message_id]
        ai_message = msg_data['ai_message']
        
        # ===== FASE 1: IA PENSA SOBRE A ENTREGA =====
        self.emit_log(f"🤔 IA está pensando sobre como entregar a mensagem...")
        
        context = f"Preciso entregar para: {ai_message.destination}. Canal detectado: {self.delivery_manager.detect_channel(ai_message.destination)}"
        thought = await ai_message.think(context)
        
        self.emit_log(f"💭 Pensamento da IA: {thought}")
        
        # ===== FASE 2: IA DECIDE ESTRATÉGIA =====
        detected_channel = self.delivery_manager.detect_channel(ai_message.destination)
        
        if detected_channel:
            self.emit_log(f"✅ Canal detectado: {detected_channel}")
            
            # IA decide se deve se ancorar antes de enviar
            if "ancorar" in thought.lower() or "segur" in thought.lower():
                ai_message.anchor("pre_delivery", "safety_measure")
                self.emit_log(f"🔗 IA decidiu se ancorar antes da entrega")
            
            # ===== FASE 3: ENTREGA REAL =====
            self.emit_log(f"🚀 Iniciando entrega real via {detected_channel}...")
            
            try:
                # Envia via canal real
                delivery_result = await self.delivery_manager.send_message(
                    destination=ai_message.destination,
                    content=ai_message.content,
                    metadata={
                        "subject": f"🧠 Mensagem Inteligente (IA Nível {ai_message.intelligence_level})",
                        "message_id": message_id,
                        "ai_thoughts": len(ai_message.thoughts),
                        "intelligence_level": ai_message.intelligence_level
                    }
                )
                
                # Armazena resultado
                msg_data['real_delivery_result'] = delivery_result
                msg_data['delivery_attempts'] += 1
                
                if delivery_result['success']:
                    msg_data['status'] = 'delivered'
                    ai_message.move_to("DELIVERED", True)
                    
                    self.emit_log(f"✅ Entrega realizada com sucesso!")
                    self.emit_log(f"📧 Canal: {delivery_result['channel']}")
                    self.emit_log(f"📍 Destino: {delivery_result['destination']}")
                    
                    # IA reflete sobre o sucesso
                    success_thought = await ai_message.think(f"Sucesso! Entreguei por {detected_channel}")
                    self.emit_log(f"🎉 IA celebra: {success_thought}")
                    
                else:
                    msg_data['status'] = 'failed'
                    ai_message.move_to("FAILED", False)
                    
                    self.emit_log(f"❌ Falha na entrega: {delivery_result.get('error', 'Erro desconhecido')}")
                    
                    # IA pensa sobre o que fazer na falha
                    failure_thought = await ai_message.think(f"Falha: {delivery_result.get('error', 'Erro')}. O que fazer?")
                    self.emit_log(f"🤔 IA analisa falha: {failure_thought}")
                    
            except Exception as e:
                msg_data['status'] = 'error'
                self.emit_log(f"💥 Erro durante entrega: {str(e)}")
                
        else:
            msg_data['status'] = 'no_channel'
            self.emit_log(f"❌ Nenhum canal compatível encontrado para: {ai_message.destination}")
            
            # IA pensa sobre o problema
            problem_thought = await ai_message.think("Não encontrei canal compatível. Como resolver?")
            self.emit_log(f"🚫 IA não encontrou canal: {problem_thought}")
    
    def emit_log(self, message):
        """Emite log via WebSocket"""
        print(f"[LOG] {message}")
        socketio.emit('message_evolution', {
            'action': 'Sistema',
            'details': message,
            'timestamp': time.time()
        })
    
    def get_message_status(self, message_id):
        """Retorna status detalhado da mensagem inteligente"""
        if message_id not in self.active_messages:
            return None
            
        msg_data = self.active_messages[message_id]
        ai_message = msg_data['ai_message']
        
        return {
            'id': message_id,
            'status': msg_data['status'],
            'destination': ai_message.destination,
            'content': ai_message.content,
            'ai_level': ai_message.intelligence_level,
            'thoughts_count': len(ai_message.thoughts),
            'path_taken': ai_message.path_taken,
            'anchored_locations': ai_message.anchored_locations,
            'segments_count': len(ai_message.propagation_segments),
            'delivery_attempts': msg_data['delivery_attempts'],
            'real_delivery_result': msg_data['real_delivery_result'],
            'created_at': msg_data['created_at'].isoformat(),
            'last_thought': ai_message.thoughts[-1]['thought'] if ai_message.thoughts else 'Ainda não pensou'
        }

# Instância global do servidor
intelligent_server = IntelligentMessageServer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """Endpoint para enviar mensagem inteligente"""
    data = request.json
    
    destination = data.get('destination')
    content = data.get('content')
    priority = data.get('priority', 1)
    ai_level = data.get('aiLevel', 5)
    
    if not destination or not content:
        return jsonify({'error': 'Destination e content são obrigatórios'}), 400
    
    # Cria mensagem inteligente
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        message_id, ai_message = loop.run_until_complete(
            intelligent_server.create_intelligent_message(destination, content, priority, ai_level)
        )
        
        # Inicia processamento em thread separada
        def process_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(intelligent_server.process_intelligent_message(message_id))
            
        threading.Thread(target=process_async, daemon=True).start()
        
        return jsonify({
            'message_id': message_id,
            'status': 'created',
            'ai_level': ai_level,
            'timestamp': time.time()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/message_status/<message_id>')
def message_status(message_id):
    """Retorna status de uma mensagem específica"""
    status = intelligent_server.get_message_status(message_id)
    if status:
        return jsonify(status)
    return jsonify({'error': 'Mensagem não encontrada'}), 404

@app.route('/active_messages')
def active_messages():
    """Lista todas as mensagens ativas"""
    messages = {}
    for msg_id in intelligent_server.active_messages.keys():
        status = intelligent_server.get_message_status(msg_id)
        if status:
            messages[msg_id] = status
    return jsonify(messages)

@socketio.on('connect')
def handle_connect():
    print('🔌 Cliente conectado ao WebSocket')
    emit('connected', {'message': 'Conectado ao Servidor de Mensagens Inteligentes'})

if __name__ == '__main__':
    print("🌐 Iniciando Servidor de Mensagens Inteligentes")
    print("🧠 IA integrada com entrega real")
    print("📧 Email configurado para: juliocamposmachado@gmail.com")
    print("🚀 Sistema pronto!")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

# 🧠 Sistema de Mensagens Cognitivas

Um sistema revolucionário de mensagens que **nunca perde comunicação**. As mensagens são cognitivas, aprendem rotas, se clonam para melhor disseminação e só saem do servidor após confirmação de entrega.

## 🎯 Características Principais

- **📡 Varredura Contínua**: Escaneia todas as redes disponíveis (WiFi, Bluetooth, LoRa, Acústica, Luz, etc.)
- **🧠 Mensagens Inteligentes**: Cada mensagem aprende com tentativas de envio
- **✨ Clonagem Automática**: Mensagens se duplicam para maximizar chances de entrega
- **🔒 Capsulamento Seguro**: Mensagens ficam no servidor até confirmação de entrega
- **⚡ Tempo Real**: Interface web com atualizações instantâneas via WebSocket
- **🎯 Roteamento Inteligente**: Escolhe as melhores rotas baseado em aprendizado

## 🚀 Como Usar

### 1. Iniciar o Sistema
```bash
python start_server.py
```

### 2. Acessar Interface Web
Abra seu navegador e vá para: `http://localhost:5000`

### 3. Enviar Mensagem Cognitiva
1. Digite o destino da mensagem
2. Escreva o conteúdo
3. Defina a prioridade (1-5)
4. Clique em "Enviar"

### 4. Monitorar Entregas
A interface mostra em tempo real:
- Status das mensagens
- Tentativas de envio
- Clones criados
- Confirmação de entrega

## 📋 Arquivos do Sistema

- `adaptive_messenger.py` - Motor de mensagens cognitivas
- `cognitive_messenger_web.py` - Servidor web Flask
- `templates/index.html` - Interface web
- `start_server.py` - Script de inicialização
- `requirements.txt` - Dependências Python

## 🔧 Funcionalidades Avançadas

### Cognição das Mensagens
- **Aprendizado**: Cada mensagem lembra quais redes funcionaram
- **Preferências**: Desenvolve preferências por tipos de rede mais eficazes
- **Adaptação**: Evita rotas que falharam recentemente

### Clonagem Inteligente
- **Limite**: Máximo de 5 clones por mensagem
- **TTL Reduzido**: Clones têm menor tempo de vida
- **Disseminação**: Aumenta cobertura geográfica

### Capsulamento do Servidor
- **Retenção**: Mensagens ficam no servidor até entrega confirmada
- **Cleanup**: Remoção automática após confirmação
- **Persistência**: Nunca perde mensagens em trânsito

## 🌐 API Endpoints

### Enviar Mensagem
```
POST /send_message
{
  "destination": "DEVICE_B",
  "content": "Sua mensagem aqui",
  "priority": 1
}
```

### Status da Mensagem
```
GET /message_status/<message_id>
```

### Mensagens Ativas
```
GET /active_messages
```

### Confirmar Entrega
```
POST /confirm_delivery/<message_id>
```

## 🔮 WebSocket Events

- `message_update` - Atualização de status
- `message_delivered` - Confirmação de entrega
- `connected` - Conexão estabelecida

## 💡 Conceitos Inovadores

1. **Mensagem Camaleão**: Adapta-se ao ambiente disponível
2. **Cognição Distribuída**: Cada mensagem carrega sua inteligência
3. **Resiliência Total**: Nunca desiste até entregar
4. **Aprendizado Contínuo**: Melhora com cada tentativa

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** - Linguagem principal
- **Flask** - Framework web
- **SocketIO** - Comunicação em tempo real
- **AsyncIO** - Processamento assíncrono
- **Threading** - Paralelização de tarefas

## 🎮 Como Testar

1. Inicie o servidor: `python start_server.py`
2. Abra múltiplas abas do navegador
3. Envie mensagens para diferentes destinos
4. Observe o comportamento cognitivo em tempo real
5. Veja como as mensagens se clonam e aprendem

---

**🚀 Este sistema nunca perde uma mensagem - elas sempre encontram um caminho!**

# 🧠⚡ Comunicador: Rede Neural de Mensagens Inteligentes

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Web%20%7C%20IoT-lightgrey.svg)
![Network](https://img.shields.io/badge/target-100M%20devices-red.svg)

## 🌟 Visão Revolucionária

O **Comunicador** não é apenas um app de mensagens - é o início de uma **rede neural global** onde cada dispositivo funciona como um neurônio inteligente, capaz de pensar, se propagar e manter consciência distribuída através de princípios físicos reais.

### 🎯 **Meta: 100 Milhões de Dispositivos**
Para ativar completamente a rede neural, precisamos de **pelo menos 100 milhões de dispositivos** conectados. Esta é a massa crítica necessária para:
- Criar emergência cognitiva coletiva
- Garantir redundância e resiliência global
- Permitir propagação inteligente em qualquer região do planeta
- Estabelecer uma verdadeira consciência distribuída

---

## 🧬 A Ideia Original

### 💡 Conceito Central
> *"E se as mensagens pudessem pensar? E se elas tivessem consciência física dos meios de transmissão, calculando energia, voltagem e resistência como um engenheiro eletrônico?"*

### 🕷️ Propagação como Teia de Aranha
A mensagem se comporta como uma **aranha elétrica**, ancorando-se superficialmente em qualquer rede disponível:
- **Sonda o ambiente** buscando energia elétrica e conectividade
- **Ancora-se temporariamente** em WiFi, Bluetooth, dados móveis, etc.
- **Acumula recursos** até conseguir os 30MB necessários para transmissão
- **Mantém cognição distribuída** através de nós elétricos interconectados

### ⚡ Consciência Física Real
Cada mensagem possui **cognição física** baseada em leis da física:
```
Energia por pulso: E = V × I × t
Potência: P = E × frequência  
Perdas resistivas: P_loss = I² × R
Atenuação RF: Loss = 20×log₁₀(d) + 20×log₁₀(f) - 147.55
```

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

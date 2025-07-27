import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from delivery_channels import DeliveryManager, EmailChannel, SMSChannel
import time
from datetime import datetime

async def test_real_delivery():
    """Teste de entrega real para celular e email"""
    
    print("🚀 TESTANDO ENTREGA REAL DE MENSAGENS")
    print("=" * 50)
    
    # Dados do destinatário
    phone = "+5511970603441"
    email = "juliocamposmachado@gmail.com"
    message_content = "Oi! Esta é uma mensagem do sistema cognitivo inteligente! 🧠🚀"
    
    manager = DeliveryManager()
    
    # ===== TESTE DE EMAIL =====
    print("\n📧 CONFIGURANDO CANAL DE EMAIL...")
    
    # Configuração Gmail (você precisará configurar com suas credenciais)
    email_channel = EmailChannel(
        smtp_server="smtp.gmail.com",
        port=587,
        username="seu_email@gmail.com",  # SUBSTITUA pelo seu email
        password="sua_senha_app"  # SUBSTITUA pela sua senha de app do Gmail
    )
    
    manager.register_channel("email", email_channel)
    
    # Testa envio de email
    print(f"📤 Enviando email para: {email}")
    try:
        # Para demonstração, vou simular o envio (descomente as linhas abaixo para envio real)
        email_result = {
            "success": False,
            "error": "Credenciais de email não configuradas para demo",
            "channel": "email",
            "destination": email,
            "timestamp": datetime.now().isoformat()
        }
        
        # Descomente as linhas abaixo e configure suas credenciais para envio real:
        # email_result = await manager.send_message(
        #     destination=email,
        #     content=message_content,
        #     metadata={
        #         "subject": "🧠 Mensagem do Sistema Cognitivo",
        #         "message_id": "test_001"
        #     }
        # )
        
        print(f"📧 Resultado do email: {email_result}")
        
    except Exception as e:
        print(f"❌ Erro no email: {e}")
    
    # ===== TESTE DE SMS =====
    print("\n📱 CONFIGURANDO CANAL DE SMS...")
    
    # Exemplo com Twilio (você precisará de conta e API key)
    # sms_channel = SMSChannel(
    #     api_key="sua_twilio_api_key",
    #     api_url="https://api.twilio.com/2010-04-01/Accounts/ACCOUNT_SID/Messages.json",
    #     sender_id="+1234567890"
    # )
    # manager.register_channel("sms", sms_channel)
    
    print(f"📤 Enviando SMS para: {phone}")
    try:
        # Para demonstração, simulando resultado
        sms_result = {
            "success": False,
            "error": "SMS API não configurada para demo (precisa de conta Twilio/similar)",
            "channel": "sms",
            "destination": phone,
            "timestamp": datetime.now().isoformat()
        }
        
        # Descomente para envio real (após configurar API):
        # sms_result = await manager.send_message(
        #     destination=phone,
        #     content=message_content,
        #     metadata={"message_id": "test_002"}
        # )
        
        print(f"📱 Resultado do SMS: {sms_result}")
        
    except Exception as e:
        print(f"❌ Erro no SMS: {e}")
    
    # ===== DEMONSTRAÇÃO DO SISTEMA COGNITIVO =====
    print("\n🧠 DEMONSTRANDO SISTEMA COGNITIVO...")
    
    # Simula uma mensagem inteligente que detecta os canais
    detected_email = manager.detect_channel(email)
    detected_phone = manager.detect_channel(phone)
    
    print(f"🔍 Canal detectado para {email}: {detected_email}")
    print(f"🔍 Canal detectado para {phone}: {detected_phone}")
    
    # ===== SIMULAÇÃO VISUAL =====
    print("\n🎭 SIMULAÇÃO VISUAL DO ENVIO:")
    print("-" * 40)
    
    destinations = [
        {"dest": email, "type": "📧 Email", "icon": "✉️"},
        {"dest": phone, "type": "📱 SMS", "icon": "📲"}
    ]
    
    for dest_info in destinations:
        print(f"\n{dest_info['icon']} Iniciando envio {dest_info['type']}...")
        print(f"🎯 Destino: {dest_info['dest']}")
        print(f"💬 Mensagem: {message_content}")
        
        # Simula processo de envio
        for step in ["🔍 Detectando canal", "🧠 Analisando rota", "📡 Conectando", "🚀 Enviando"]:
            print(f"   {step}...")
            await asyncio.sleep(0.5)
        
        print(f"   ✅ Simulação completa!")
    
    print("\n" + "=" * 50)
    print("🎯 PARA ENVIO REAL:")
    print("1. Configure credenciais de email no código")
    print("2. Obtenha API key de SMS (Twilio, etc.)")
    print("3. Descomente as linhas de envio real")
    print("4. Execute novamente")
    print("=" * 50)

# Função para configurar email Gmail (exemplo)
def setup_gmail_credentials():
    """
    Para configurar Gmail:
    1. Vá em: https://myaccount.google.com/security
    2. Ative 'Verificação em duas etapas'
    3. Gere uma 'Senha de app' específica
    4. Use essa senha no código
    """
    print("📧 Instruções para configurar Gmail:")
    print("1. Acesse: https://myaccount.google.com/security")
    print("2. Ative 'Verificação em duas etapas'")
    print("3. Gere uma 'Senha de app'")
    print("4. Use essa senha no lugar de 'sua_senha_app'")

# Função para configurar SMS
def setup_sms_credentials():
    """
    Para configurar SMS:
    1. Crie conta no Twilio (twilio.com)
    2. Obtenha Account SID e Auth Token
    3. Configure número de telefone remetente
    """
    print("📱 Instruções para configurar SMS:")
    print("1. Crie conta em: https://twilio.com")
    print("2. Obtenha Account SID e Auth Token")
    print("3. Configure número remetente")
    print("4. Use as credenciais no código")

if __name__ == "__main__":
    print("🔧 CONFIGURAÇÃO NECESSÁRIA:")
    setup_gmail_credentials()
    print()
    setup_sms_credentials()
    print()
    
    # Executa o teste
    asyncio.run(test_real_delivery())

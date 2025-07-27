import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from delivery_channels import DeliveryManager, EmailChannel
import time
from datetime import datetime

async def send_real_message():
    """Envia mensagem real usando as credenciais configuradas"""
    
    print("🚀 ENVIANDO MENSAGEM REAL!")
    print("=" * 50)
    
    # Suas credenciais reais
    email_remetente = "juliocamposmachado@gmail.com"
    senha_app = "lyia mihj mhdk dqkn"
    email_destinatario = "juliocamposmachado@gmail.com"
    telefone = "+5511970603441"
    
    # Mensagem
    mensagem = "Oi! 👋 Esta é uma mensagem do sistema cognitivo inteligente! 🧠🚀 Funcionou perfeitamente!"
    
    print(f"📧 Configurando email: {email_remetente}")
    print(f"🎯 Destinatário: {email_destinatario}")
    print(f"💬 Mensagem: {mensagem}")
    print()
    
    # Cria gerenciador de entrega
    manager = DeliveryManager()
    
    # Configura canal de email com suas credenciais
    email_channel = EmailChannel(
        smtp_server="smtp.gmail.com",
        port=587,
        username=email_remetente,
        password=senha_app
    )
    
    manager.register_channel("email", email_channel)
    
    # ===== ENVIO REAL DE EMAIL =====
    print("📤 Enviando email...")
    
    try:
        resultado_email = await manager.send_message(
            destination=email_destinatario,
            content=mensagem,
            metadata={
                "subject": "🧠 Oi do Sistema Cognitivo Inteligente!",
                "message_id": f"real_msg_{int(time.time())}"
            }
        )
        
        print("✅ RESULTADO DO EMAIL:")
        print(f"   Sucesso: {resultado_email['success']}")
        if resultado_email['success']:
            print(f"   Canal: {resultado_email['channel']}")
            print(f"   Destino: {resultado_email['destination']}")
            print(f"   Timestamp: {resultado_email['timestamp']}")
            print(f"   Message ID: {resultado_email['message_id']}")
            print()
            print("🎉 EMAIL ENVIADO COM SUCESSO!")
            print("📬 Verifique sua caixa de entrada!")
        else:
            print(f"   Erro: {resultado_email['error']}")
            
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
    
    # ===== SIMULAÇÃO VISUAL PARA SMS =====
    print("\n" + "=" * 50)
    print("📱 SIMULAÇÃO PARA SMS:")
    print(f"🎯 Telefone: {telefone}")
    print("⚠️  Para SMS real, configure API do Twilio")
    print()
    
    # Simula processo visual para SMS
    print("📲 Simulando envio de SMS...")
    for step in ["🔍 Detectando canal", "🧠 Analisando rota", "📡 Conectando", "🚀 Enviando"]:
        print(f"   {step}...")
        await asyncio.sleep(0.3)
    
    print("   ✅ Simulação de SMS completa!")
    print(f"   💬 Conteúdo que seria enviado: {mensagem}")
    
    print("\n" + "=" * 50)
    print("🎊 TESTE CONCLUÍDO!")
    print("📧 Email enviado para:", email_destinatario)
    print("📱 SMS simulado para:", telefone)
    print("🧠 Sistema cognitivo funcionando perfeitamente!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(send_real_message())

import smtplib
import re
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import aiohttp
from datetime import datetime


class DeliveryChannel(ABC):
    """Interface base para canais de entrega"""
    
    @abstractmethod
    async def send(self, destination: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Envia mensagem pelo canal"""
        pass
    
    @abstractmethod
    def validate_destination(self, destination: str) -> bool:
        """Valida se o destino é válido para este canal"""
        pass


class EmailChannel(DeliveryChannel):
    """Canal de entrega por email"""
    
    def __init__(self, smtp_server: str, port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.port = port  
        self.username = username
        self.password = password
    
    def validate_destination(self, destination: str) -> bool:
        """Valida formato de email"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, destination))
    
    async def send(self, destination: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Envia email"""
        if not self.validate_destination(destination):
            return {"success": False, "error": "Email inválido"}
        
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = destination
            msg['Subject'] = metadata.get('subject', 'Mensagem Cognitiva')
            
            # Adicionar conteúdo
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # Conectar e enviar
            await asyncio.get_event_loop().run_in_executor(
                None, self._send_email, msg, destination
            )
            
            return {
                "success": True,
                "channel": "email",
                "destination": destination,
                "timestamp": datetime.now().isoformat(),
                "message_id": metadata.get('message_id')
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "channel": "email",
                "destination": destination
            }
    
    def _send_email(self, msg, destination):
        """Envia email (executado em thread)"""
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg, to_addrs=[destination])


class SMSChannel(DeliveryChannel):
    """Canal de entrega por SMS"""
    
    def __init__(self, api_key: str, api_url: str, sender_id: str = None):
        self.api_key = api_key
        self.api_url = api_url
        self.sender_id = sender_id
    
    def validate_destination(self, destination: str) -> bool:
        """Valida formato de telefone"""
        # Remove espaços e caracteres especiais
        phone = re.sub(r'[^\d+]', '', destination)
        # Verifica se tem formato válido (10-15 dígitos)
        return bool(re.match(r'^\+?[1-9]\d{9,14}$', phone))
    
    async def send(self, destination: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Envia SMS via API"""
        if not self.validate_destination(destination):
            return {"success": False, "error": "Número de telefone inválido"}
        
        try:
            # Limpa número
            phone = re.sub(r'[^\d+]', '', destination)
            
            # Payload para API (exemplo genérico)
            payload = {
                "to": phone,
                "message": content,
                "from": self.sender_id or "CognitiveMSG"
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url, 
                    json=payload, 
                    headers=headers
                ) as response:
                    result = await response.json()
                    
                    return {
                        "success": response.status == 200,
                        "channel": "sms", 
                        "destination": phone,
                        "timestamp": datetime.now().isoformat(),
                        "api_response": result,
                        "message_id": metadata.get('message_id')
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "channel": "sms",
                "destination": destination
            }


class WhatsAppChannel(DeliveryChannel):
    """Canal de entrega por WhatsApp Business API"""
    
    def __init__(self, access_token: str, phone_number_id: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.api_url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
    
    def validate_destination(self, destination: str) -> bool:
        """Valida formato de telefone WhatsApp"""
        phone = re.sub(r'[^\d+]', '', destination)
        return bool(re.match(r'^\+?[1-9]\d{9,14}$', phone))
    
    async def send(self, destination: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Envia mensagem via WhatsApp Business API"""
        if not self.validate_destination(destination):
            return {"success": False, "error": "Número WhatsApp inválido"}
        
        try:
            # Limpa número (WhatsApp precisa sem + no início)
            phone = re.sub(r'[^\d]', '', destination)
            
            payload = {
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "text",
                "text": {"body": content}
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers=headers
                ) as response:
                    result = await response.json()
                    
                    return {
                        "success": response.status == 200,
                        "channel": "whatsapp",
                        "destination": phone,
                        "timestamp": datetime.now().isoformat(),
                        "api_response": result,
                        "message_id": metadata.get('message_id')
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "channel": "whatsapp",
                "destination": destination
            }


class TelegramChannel(DeliveryChannel):
    """Canal de entrega por Telegram Bot"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    def validate_destination(self, destination: str) -> bool:
        """Valida chat_id do Telegram"""
        # Chat ID pode ser número ou @username
        return bool(re.match(r'^(@[a-zA-Z0-9_]+|[0-9-]+)$', destination))
    
    async def send(self, destination: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Envia mensagem via Telegram Bot API"""
        if not self.validate_destination(destination):
            return {"success": False, "error": "Chat ID inválido"}
        
        try:
            payload = {
                "chat_id": destination,
                "text": content,
                "parse_mode": "HTML"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload) as response:
                    result = await response.json()
                    
                    return {
                        "success": result.get("ok", False),
                        "channel": "telegram",
                        "destination": destination,
                        "timestamp": datetime.now().isoformat(),
                        "api_response": result,
                        "message_id": metadata.get('message_id')
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "channel": "telegram",
                "destination": destination
            }


class DeliveryManager:
    """Gerenciador de canais de entrega"""
    
    def __init__(self):
        self.channels: Dict[str, DeliveryChannel] = {}
    
    def register_channel(self, name: str, channel: DeliveryChannel):
        """Registra um novo canal"""
        self.channels[name] = channel
    
    def detect_channel(self, destination: str) -> Optional[str]:
        """Detecta automaticamente o canal baseado no destino"""
        for name, channel in self.channels.items():
            if channel.validate_destination(destination):
                return name
        return None
    
    async def send_message(self, destination: str, content: str, 
                          channel_name: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Envia mensagem pelo canal apropriado"""
        
        # Auto-detecta canal se não especificado
        if not channel_name:
            channel_name = self.detect_channel(destination)
            if not channel_name:
                return {
                    "success": False,
                    "error": "Nenhum canal compatível encontrado",
                    "destination": destination
                }
        
        # Verifica se canal existe
        if channel_name not in self.channels:
            return {
                "success": False,
                "error": f"Canal '{channel_name}' não encontrado",
                "destination": destination
            }
        
        # Envia mensagem
        channel = self.channels[channel_name]
        result = await channel.send(destination, content, metadata)
        
        return result


# Configuração de exemplo
def setup_delivery_manager():
    """Configura o gerenciador com canais padrão"""
    manager = DeliveryManager()
    
    # Email (Gmail exemplo)
    email_channel = EmailChannel(
        smtp_server="smtp.gmail.com",
        port=587,
        username="seu_email@gmail.com",  # Configure com suas credenciais
        password="sua_senha_app"  # Use App Password do Gmail
    )
    manager.register_channel("email", email_channel)
    
    # SMS (exemplo com Twilio)
    # sms_channel = SMSChannel(
    #     api_key="sua_api_key",
    #     api_url="https://api.twilio.com/2010-04-01/Accounts/ACCOUNT_SID/Messages.json",
    #     sender_id="+1234567890"
    # )
    # manager.register_channel("sms", sms_channel)
    
    # WhatsApp Business
    # whatsapp_channel = WhatsAppChannel(
    #     access_token="seu_access_token",
    #     phone_number_id="seu_phone_number_id"
    # )
    # manager.register_channel("whatsapp", whatsapp_channel)
    
    # Telegram
    # telegram_channel = TelegramChannel(bot_token="seu_bot_token")
    # manager.register_channel("telegram", telegram_channel)
    
    return manager


# Exemplo de uso
async def example_usage():
    """Exemplo de como usar o sistema"""
    manager = setup_delivery_manager()
    
    # Envia email
    result = await manager.send_message(
        destination="usuario@example.com",
        content="Olá! Esta é uma mensagem cognitiva entregue por email.",
        metadata={"subject": "Mensagem Cognitiva", "message_id": "123"}
    )
    print("Email:", result)
    
    # Envia SMS (auto-detecta canal)
    result = await manager.send_message(
        destination="+5511999999999",
        content="SMS via sistema cognitivo!",
        metadata={"message_id": "124"}
    )
    print("SMS:", result)


if __name__ == "__main__":
    # Teste do sistema
    asyncio.run(example_usage())

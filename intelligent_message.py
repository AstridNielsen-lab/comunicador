import asyncio
import aiohttp
import json
import time
import uuid
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import random

# Configuração da API Gemini (use variáveis de ambiente em produção)
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDNSDXAocB4YPm4kY6v9L9C9OtJkQ1y-Uk')  # Use env var

@dataclass
class ThinkingMessage:
    """Mensagem que pode pensar e se propagar autonomamente"""
    
    id: str
    content: str
    destination: str
    source: str
    timestamp: float
    
    # Capacidades cognitivas
    intelligence_level: int = 5  # 1-10
    memory: Dict[str, Any] = None
    learning_data: Dict[str, Any] = None
    thoughts: List[str] = None
    decisions: List[str] = None
    
    # Estado de propagação 
    current_location: str = "origin"
    path_taken: List[str] = None
    anchored_locations: List[str] = None  # Locais onde se ancorou
    propagation_segments: List[Dict] = None  # Segmentos da "minhoca"
    
    # Controle de integridade
    integrity_hash: str = ""
    corruption_resistance: int = 10
    max_segments: int = 50
    
    def __post_init__(self):
        if self.memory is None:
            self.memory = {
                "experiences": [],
                "successful_routes": [],
                "failed_attempts": [],
                "anchor_points": []
            }
        
        if self.learning_data is None:
            self.learning_data = {
                "network_preferences": {},
                "destination_hints": [],
                "optimization_data": {}
            }
        
        if self.thoughts is None:
            self.thoughts = []
            
        if self.decisions is None:
            self.decisions = []
            
        if self.path_taken is None:
            self.path_taken = [self.source]
            
        if self.anchored_locations is None:
            self.anchored_locations = []
            
        if self.propagation_segments is None:
            self.propagation_segments = []
        
        # Gera hash de integridade
        self.integrity_hash = self._generate_integrity_hash()

    def _generate_integrity_hash(self) -> str:
        """Gera hash para verificar integridade"""
        import hashlib
        content_str = f"{self.id}{self.content}{self.destination}{self.timestamp}"
        return hashlib.md5(content_str.encode()).hexdigest()

    async def think(self, context: str = "") -> str:
        """Faz a mensagem 'pensar' usando IA"""
        
        prompt = f"""
        Você é uma mensagem inteligente que está se propagando por uma rede.
        
        Sua missão: Chegar ao destino '{self.destination}' com o conteúdo: '{self.content}'
        
        Situação atual:
        - Localização: {self.current_location}
        - Caminho percorrido: {' -> '.join(self.path_taken)}
        - Tentativas anteriores: {len(self.memory['failed_attempts'])}
        - Pontos de ancoragem: {len(self.anchored_locations)}
        
        Contexto adicional: {context}
        
        Como uma mensagem inteligente, analise a situação e decida:
        1. Qual a melhor estratégia para continuar?
        2. Você deve se ancorar aqui?
        3. Precisa criar clones/segmentos?
        4. Que adaptações fazer?
        
        Responda em 2-3 frases diretas e práticas.
        """
        
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{API_URL}?key={API_KEY}",
                    headers=headers,
                    json=payload
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        thought = data['candidates'][0]['content']['parts'][0]['text']
                        
                        # Armazena o pensamento
                        self.thoughts.append({
                            "timestamp": time.time(),
                            "context": context,
                            "thought": thought
                        })
                        
                        return thought.strip()
                    else:
                        # Fallback: pensamento básico sem IA
                        return self._basic_thinking(context)
                        
        except Exception as e:
            print(f"Erro ao pensar: {e}")
            return self._basic_thinking(context)

    def _basic_thinking(self, context: str) -> str:
        """Pensamento básico sem IA como fallback"""
        if len(self.memory['failed_attempts']) > 3:
            return "Muitas falhas. Vou me ancorar e criar clones para explorar rotas paralelas."
        elif self.current_location == self.destination:
            return "Chegei ao destino! Missão cumprida."
        else:
            return "Analisando rede local. Procurando melhor rota para o destino."

    def anchor(self, location: str, reason: str = "strategic"):
        """Ancora a mensagem em um local"""
        if location not in self.anchored_locations:
            self.anchored_locations.append(location)
            self.memory["anchor_points"].append({
                "location": location,
                "timestamp": time.time(),
                "reason": reason
            })
            
            print(f"🔗 Mensagem {self.id[:8]} ancorada em {location} ({reason})")

    def create_segment(self, target_location: str) -> 'ThinkingMessage':
        """Cria um novo segmento da mensagem (como minhoca se estendendo)"""
        if len(self.propagation_segments) >= self.max_segments:
            return None
            
        # Cria um novo segmento conectado
        segment = ThinkingMessage(
            id=f"{self.id}_seg_{len(self.propagation_segments)}",
            content=self.content,
            destination=self.destination,
            source=self.current_location,
            timestamp=time.time(),
            intelligence_level=self.intelligence_level,
            memory=self.memory.copy(),
            learning_data=self.learning_data.copy()
        )
        
        segment.current_location = target_location
        segment.path_taken = self.path_taken + [target_location]
        
        # Registra o segmento
        self.propagation_segments.append({
            "segment_id": segment.id,
            "created_at": time.time(),
            "target": target_location,
            "status": "active"
        })
        
        print(f"🪱 Segmento criado: {segment.id} -> {target_location}")
        return segment

    def retract_segment(self, segment_id: str, reason: str = "failure"):
        """Retrai um segmento da minhoca"""
        for segment in self.propagation_segments:
            if segment["segment_id"] == segment_id:
                segment["status"] = "retracted"
                segment["retracted_at"] = time.time()
                segment["reason"] = reason
                
                print(f"↩️ Segmento {segment_id} retraído: {reason}")
                break

    def verify_integrity(self) -> bool:
        """Verifica se a mensagem não foi corrompida"""
        current_hash = self._generate_integrity_hash()
        return current_hash == self.integrity_hash

    def move_to(self, new_location: str, success: bool = True):
        """Move a mensagem para uma nova localização"""
        old_location = self.current_location
        self.current_location = new_location
        
        if new_location not in self.path_taken:
            self.path_taken.append(new_location)
        
        # Registra experiência
        experience = {
            "from": old_location,
            "to": new_location,
            "timestamp": time.time(),
            "success": success
        }
        
        if success:
            self.memory["successful_routes"].append(experience)
        else:
            self.memory["failed_attempts"].append(experience)
            
        print(f"📍 Mensagem {self.id[:8]} movida: {old_location} -> {new_location}")

    async def autonomous_propagation(self, available_networks: List[str], 
                                   socketio_callback=None) -> bool:
        """Propagação autônoma da mensagem"""
        
        # Pensa sobre a situação atual
        context = f"Redes disponíveis: {available_networks}"
        thought = await self.think(context)
        
        print(f"🧠 Pensamento: {thought}")
        
        # Emite log se callback disponível
        if socketio_callback:
            socketio_callback('message_evolution', {
                'message_id': self.id,
                'action': 'Pensando',
                'details': thought,
                'location': self.current_location
            })
        
        # Decide ação baseada no pensamento
        if "ancorar" in thought.lower():
            self.anchor(self.current_location, "strategic_decision")
            
        if "clone" in thought.lower() or "segmento" in thought.lower():
            # Cria segmentos para explorar múltiplas rotas
            for network in available_networks[:2]:  # Máximo 2 segmentos
                segment = self.create_segment(f"via_{network}")
                if segment and socketio_callback:
                    socketio_callback('message_clone', {
                        'original_id': self.id,
                        'segment_id': segment.id,
                        'clone_number': len(self.propagation_segments)
                    })
        
        # Tenta se mover para o destino
        if available_networks:
            chosen_network = random.choice(available_networks)
            success = random.random() > 0.3  # 70% chance de sucesso
            
            if socketio_callback:
                socketio_callback('message_route_attempt', {
                    'message_id': self.id,
                    'network_type': chosen_network,
                    'next_hop': f"node_via_{chosen_network}",
                    'success': success
                })
            
            if success:
                self.move_to(f"node_via_{chosen_network}", True)
                
                # Verifica se chegou ao destino
                if self.current_location == self.destination:
                    if socketio_callback:
                        socketio_callback('message_delivered', {
                            'message_id': self.id,
                            'timestamp': time.time()
                        })
                    return True
            else:
                self.move_to(f"failed_{chosen_network}", False)
                
        return False

    def get_status_report(self) -> Dict[str, Any]:
        """Relatório completo do status da mensagem"""
        return {
            "id": self.id,
            "content": self.content,
            "destination": self.destination,
            "current_location": self.current_location,
            "intelligence_level": self.intelligence_level,
            "path_taken": self.path_taken,
            "anchored_locations": self.anchored_locations,
            "segments_count": len(self.propagation_segments),
            "thoughts_count": len(self.thoughts),
            "successful_routes": len(self.memory["successful_routes"]),
            "failed_attempts": len(self.memory["failed_attempts"]),
            "integrity_verified": self.verify_integrity(),
            "last_thought": self.thoughts[-1]["thought"] if self.thoughts else "Ainda não pensou",
            "created_at": datetime.fromtimestamp(self.timestamp).isoformat()
        }


# Exemplo de uso e teste
async def test_intelligent_message():
    """Teste da mensagem inteligente"""
    
    # Cria mensagem inteligente
    message = ThinkingMessage(
        id=str(uuid.uuid4()),
        content="Esta é uma mensagem que pode pensar!",
        destination="servidor_destino",
        source="origem",
        timestamp=time.time()
    )
    
    print("🚀 Iniciando teste de mensagem inteligente")
    print(f"ID: {message.id}")
    
    # Simula redes disponíveis
    networks = ["wifi", "bluetooth", "lora", "mesh"]
    
    # Executa propagação autônoma
    for i in range(5):
        print(f"\n--- Ciclo {i+1} ---")
        
        delivered = await message.autonomous_propagation(networks)
        
        if delivered:
            print("✅ Mensagem entregue com sucesso!")
            break
            
        # Simula mudança de ambiente
        networks = random.sample(["wifi", "bluetooth", "lora", "mesh", "cellular"], 3)
        await asyncio.sleep(1)
    
    # Relatório final
    print("\n📊 Relatório Final:")
    report = message.get_status_report()
    for key, value in report.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(test_intelligent_message())

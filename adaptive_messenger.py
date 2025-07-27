import asyncio
import json
import time
import uuid
import threading
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib

class NetworkType(Enum):
    WIFI = "wifi"
    BLUETOOTH = "bluetooth" 
    LORA = "lora"
    ACOUSTIC = "acoustic"
    LIGHT = "light"
    MESH = "mesh"
    CELLULAR = "cellular"
    RADIO = "radio"

@dataclass
class Message:
    id: str
    source: str
    destination: str
    content: str
    timestamp: float
    ttl: int = 100  # Time to live (hops)
    path: List[str] = None
    priority: int = 1
    cognizant: bool = True  # Cognitivo: Clona-se nas bases
    deliveries: Set[str] = None  # Dispositivos que receberam com sucesso
    clone_count: int = 0  # Quantas vezes foi clonada
    learning_data: Dict = None  # Dados de aprendizado da rota
    
    def __post_init__(self):
        if self.deliveries is None:
            self.deliveries = set()
        if self.path is None:
            self.path = []
        if self.learning_data is None:
            self.learning_data = {
                'successful_routes': [],
                'failed_routes': [],
                'network_preferences': {},
                'destination_hints': []
            }

@dataclass
class NetworkRoute:
    network_type: NetworkType
    signal_strength: float
    latency: float
    available: bool
    next_hop: Optional[str] = None
    cost: float = 1.0

class AdaptiveMessenger:
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.message_queue: List[Message] = []
        self.known_routes: Dict[str, List[NetworkRoute]] = {}
        self.network_scanners = {}
        self.is_scanning = False
        self.message_cache: Set[str] = set()  # Para evitar loops
        
    async def start(self):
        """Inicia o sistema de varredura e roteamento"""
        print(f"[{self.device_id}] Sistema iniciado - Varrendo todas as redes...")
        
        # Inicia scanners em paralelo
        tasks = [
            self.scan_networks(),
            self.process_message_queue(),
            self.cleanup_cache()
        ]
        
        await asyncio.gather(*tasks)
    
    async def scan_networks(self):
        """Varre continuamente todas as redes disponíveis"""
        self.is_scanning = True
        
        while self.is_scanning:
            available_routes = []
            
            # Simula varredura de diferentes tipos de rede
            for network_type in NetworkType:
                routes = await self.scan_network_type(network_type)
                available_routes.extend(routes)
            
            # Atualiza tabela de roteamento
            await self.update_routing_table(available_routes)
            
            # Espera antes da próxima varredura
            await asyncio.sleep(2)
    
    async def scan_network_type(self, network_type: NetworkType) -> List[NetworkRoute]:
        """Simula varredura de um tipo específico de rede"""
        import random
        
        routes = []
        
        # Simula descoberta de redes/dispositivos próximos
        if random.random() > 0.3:  # 70% chance de encontrar algo
            for i in range(random.randint(1, 3)):
                route = NetworkRoute(
                    network_type=network_type,
                    signal_strength=random.uniform(0.1, 1.0),
                    latency=random.uniform(10, 500),
                    available=True,
                    next_hop=f"device_{network_type.value}_{i}",
                    cost=random.uniform(0.5, 2.0)
                )
                routes.append(route)
        
        return routes
    
    async def update_routing_table(self, routes: List[NetworkRoute]):
        """Atualiza tabela de roteamento com novas rotas descobertas"""
        current_time = time.time()
        
        for route in routes:
            if route.next_hop not in self.known_routes:
                self.known_routes[route.next_hop] = []
            
            # Remove rotas antigas do mesmo tipo
            self.known_routes[route.next_hop] = [
                r for r in self.known_routes[route.next_hop] 
                if r.network_type != route.network_type
            ]
            
            # Adiciona nova rota
            self.known_routes[route.next_hop].append(route)
        
        print(f"[{self.device_id}] Rotas descobertas: {len(routes)} - Total conhecidas: {len(self.known_routes)}")
    
    def send_message(self, destination: str, content: str, priority: int = 1):
        """Envia uma mensagem para o destino"""
        message = Message(
            id=str(uuid.uuid4()),
            source=self.device_id,
            destination=destination,
            content=content,
            timestamp=time.time(),
            priority=priority,
            path=[self.device_id]
        )
        
        self.message_queue.append(message)
        print(f"[{self.device_id}] Mensagem adicionada à fila: {message.id[:8]} -> {destination}")
    
    async def process_message_queue(self):
        """Processa fila de mensagens continuamente"""
        while True:
            if self.message_queue:
                # Ordena por prioridade
                self.message_queue.sort(key=lambda m: m.priority, reverse=True)
                
                message = self.message_queue.pop(0)
                await self.route_message(message)
            
            await asyncio.sleep(1)
    
    async def route_message(self, message: Message):
        """Encontra e executa a melhor rota para a mensagem"""
        print(f"[{self.device_id}] Roteando mensagem {message.id[:8]} para {message.destination}")
        
        # Verifica se chegou ao destino
        if message.destination == self.device_id:
            await self.deliver_message(message)
            return
        
        # Evita loops
        if message.id in self.message_cache:
            print(f"[{self.device_id}] Mensagem já processada, clonando para melhorar alcance: {message.id[:8]}")
            self.clone_message(message)
            return
        
        self.message_cache.add(message.id)
        
        # Verifica TTL
        if message.ttl <= 0:
            print(f"[{self.device_id}] TTL expirado para mensagem: {message.id[:8]}")
            return
        
        # Busca melhor rota usando aprendizado da mensagem
        if message.cognizant and message.learning_data['network_preferences']:
            best_route = await self.find_best_route_with_learning(message)
        else:
            best_route = await self.find_best_route(message.destination)
        
        if best_route:
            await self.forward_message(message, best_route)
        else:
            print(f"[{self.device_id}] Nenhuma rota encontrada, mantendo em fila: {message.id[:8]}")
            # Recoloca na fila para tentar novamente
            message.ttl -= 1
            self.message_queue.append(message)
    
    async def find_best_route(self, destination: str) -> Optional[NetworkRoute]:
        """Encontra a melhor rota para o destino"""
        if not self.known_routes:
            return None
        
        best_route = None
        best_score = float('inf')
        
        # Avalia todas as rotas conhecidas
        for next_hop, routes in self.known_routes.items():
            for route in routes:
                if route.available:
                    # Score baseado em latência, força do sinal e custo
                    score = (route.latency * route.cost) / route.signal_strength
                    
                    if score < best_score:
                        best_score = score
                        best_route = route
        
        return best_route
    
    async def forward_message(self, message: Message, route: NetworkRoute):
        """Encaminha mensagem pela rota selecionada"""
        print(f"[{self.device_id}] Encaminhando via {route.network_type.value} -> {route.next_hop}")
        
        # Adiciona este dispositivo ao caminho
        message.path.append(self.device_id)
        message.ttl -= 1
        
        # Simula envio pela rede
        success = await self.transmit_via_network(message, route)
        
        # Mensagem aprende com o resultado
        if message.cognizant:
            self.message_learns_route(message, route, success)
        
        if not success:
            print(f"[{self.device_id}] Falha na transmissão, tentando outra rota...")
            # Remove rota com falha temporariamente
            route.available = False
            # Recoloca mensagem na fila
            self.message_queue.append(message)
    
    async def transmit_via_network(self, message: Message, route: NetworkRoute) -> bool:
        """Simula transmissão pela rede específica"""
        import random
        
        # Simula delay da rede
        await asyncio.sleep(route.latency / 1000)
        
        # Simula chance de falha baseada na força do sinal
        success_rate = route.signal_strength * 0.8 + 0.2
        success = random.random() < success_rate
        
        if success:
            print(f"[{self.device_id}] ✓ Transmissão bem-sucedida via {route.network_type.value}")
            # Aqui conectaria com o próximo dispositivo da rede
        else:
            print(f"[{self.device_id}] ✗ Falha na transmissão via {route.network_type.value}")
        
        return success
    
    async def deliver_message(self, message: Message):
        """Entrega mensagem no destino final e registra entrega"""
        message.deliveries.add(self.device_id)
        print(f"[{self.device_id}] 📨 MENSAGEM ENTREGUE!")
        print(f"   ID: {message.id[:8]}")
        print(f"   De: {message.source}")
        print(f"   Para: {message.destination}")
        print(f"   Conteúdo: {message.content}")
        arrow = ' -> '
        print(f"   Caminho: {arrow.join(message.path)}")
        print(f"   Tempo: {time.time() - message.timestamp:.2f}s")
    
    def clone_message(self, message: Message):
        """Clona a mensagem cognitiva para tentar entrega em novos nós"""
        if not message.cognizant or message.clone_count >= 5:  # Limite de clones
            return
            
        # Cria uma nova cópia para tentar diferentes rotas
        clone = Message(
            id=message.id,
            source=message.source,
            destination=message.destination,
            content=message.content,
            timestamp=message.timestamp,
            ttl=max(message.ttl - 10, 20),  # Reduz TTL do clone
            path=message.path.copy(),
            priority=message.priority,
            cognizant=message.cognizant,
            deliveries=message.deliveries.copy(),
            clone_count=message.clone_count + 1,
            learning_data=message.learning_data.copy()
        )
        
        # Adiciona dados de aprendizado
        clone.learning_data['destination_hints'].append(self.device_id)
        
        self.message_queue.append(clone)
        print(f"[{self.device_id}] ✨ Mensagem clonada cognitiva #{clone.clone_count} - Disseminando inteligentemente")
    
    def message_learns_route(self, message: Message, route: NetworkRoute, success: bool):
        """Mensagem aprende sobre a eficácia das rotas"""
        route_info = {
            'network_type': route.network_type.value,
            'next_hop': route.next_hop,
            'signal_strength': route.signal_strength,
            'latency': route.latency,
            'timestamp': time.time()
        }
        
        if success:
            message.learning_data['successful_routes'].append(route_info)
            # Aumenta preferência por este tipo de rede
            network_type = route.network_type.value
            if network_type not in message.learning_data['network_preferences']:
                message.learning_data['network_preferences'][network_type] = 0
            message.learning_data['network_preferences'][network_type] += 1
        else:
            message.learning_data['failed_routes'].append(route_info)
            
        print(f"[{self.device_id}] 🧠 Mensagem aprendeu: {route.network_type.value} = {'✓' if success else '✗'}")
    
    async def find_best_route_with_learning(self, message: Message) -> Optional[NetworkRoute]:
        """Encontra a melhor rota usando dados de aprendizado da mensagem"""
        if not self.known_routes:
            return None
        
        best_route = None
        best_score = float('inf')
        
        # Avalia todas as rotas conhecidas
        for next_hop, routes in self.known_routes.items():
            for route in routes:
                if route.available:
                    # Score base
                    base_score = (route.latency * route.cost) / route.signal_strength
                    
                    # Aplica aprendizado da mensagem
                    network_pref = message.learning_data['network_preferences'].get(
                        route.network_type.value, 0
                    )
                    
                    # Bonifica redes que funcionaram antes
                    learning_bonus = 1.0 - (network_pref * 0.1)  # Até 50% de desconto
                    final_score = base_score * max(learning_bonus, 0.5)
                    
                    # Verifica se esta rota já falhou recentemente
                    recent_failures = [
                        f for f in message.learning_data['failed_routes']
                        if f['next_hop'] == route.next_hop and 
                           time.time() - f['timestamp'] < 60  # 1 minuto
                    ]
                    
                    if recent_failures:
                        final_score *= 2.0  # Penaliza rotas que falharam recentemente
                    
                    if final_score < best_score:
                        best_score = final_score
                        best_route = route
        
        return best_route
    
    async def cleanup_cache(self):
        """Limpa cache periodicamente"""
        while True:
            await asyncio.sleep(300)  # 5 minutos
            self.message_cache.clear()
            print(f"[{self.device_id}] Cache de mensagens limpo")

# Exemplo de uso
async def demo():
    # Cria dispositivos
    device_a = AdaptiveMessenger("DEVICE_A")
    device_b = AdaptiveMessenger("DEVICE_B")
    
    # Envia mensagem
    device_a.send_message("DEVICE_B", "Olá! Esta mensagem vai encontrar qualquer caminho até você!", priority=5)
    device_a.send_message("DEVICE_C", "Procurando DEVICE_C por qualquer rede disponível...", priority=3)
    
    # Inicia sistema
    await device_a.start()

if __name__ == "__main__":
    print("🚀 Iniciando Sistema de Mensagens Adaptativo")
    print("📡 Varrendo todas as redes disponíveis...")
    print("📱 Sistema nunca perde comunicação!")
    
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário")

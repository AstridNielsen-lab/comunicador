import asyncio
import json
import time
import uuid
import random
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from intelligent_message import ThinkingMessage
from delivery_channels import DeliveryManager, EmailChannel


class RealTimeLogger:
    """Sistema de logs em tempo real para mensagens inteligentes"""
    
    def __init__(self, log_callback: Optional[Callable] = None):
        self.log_callback = log_callback
        self.log_history = []
    
    def log(self, level: str, message: str, data: Dict = None):
        """Registra um log com timestamp"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        self.log_history.append(log_entry)
        
        # Emite via callback se disponível
        if self.log_callback:
            self.log_callback(log_entry)
        
        # Print para console
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌",
            "THINKING": "🧠",
            "MOVEMENT": "📍",
            "CLONE": "🔀",
            "ANCHOR": "🔗",
            "NETWORK": "📡",
            "DELIVERY": "📧"
        }
        
        emoji = emoji_map.get(level, "📝")
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {emoji} {message}")


class IntelligentNetworkSimulator:
    """Simula uma rede complexa com múltiplos nós e caminhos"""
    
    def __init__(self, logger: RealTimeLogger):
        self.logger = logger
        self.nodes = self._create_network_topology()
        self.network_conditions = {}
        self._simulate_network_conditions()
    
    def _create_network_topology(self) -> Dict[str, List[str]]:
        """Cria topologia de rede complexa"""
        topology = {
            "origin": ["gateway_1", "gateway_2", "direct_route"],
            "gateway_1": ["hub_a", "hub_b", "backup_node"],
            "gateway_2": ["hub_c", "hub_d", "mesh_cluster"],
            "direct_route": ["fast_lane", "destination"],
            "hub_a": ["relay_1", "relay_2", "destination"],
            "hub_b": ["relay_3", "satellite_node"],
            "hub_c": ["relay_4", "backup_destination"],
            "hub_d": ["mesh_cluster", "destination"],
            "mesh_cluster": ["mesh_1", "mesh_2", "mesh_3"],
            "mesh_1": ["destination", "backup_destination"],
            "mesh_2": ["relay_5", "destination"],
            "mesh_3": ["satellite_node", "destination"],
            "fast_lane": ["destination"],
            "relay_1": ["destination"],
            "relay_2": ["destination"],
            "relay_3": ["destination"],
            "relay_4": ["destination"],
            "relay_5": ["destination"],
            "satellite_node": ["destination"],
            "backup_node": ["backup_destination"],
            "backup_destination": ["destination"]
        }
        
        self.logger.log("INFO", f"Topologia de rede criada com {len(topology)} nós")
        return topology
    
    def _simulate_network_conditions(self):
        """Simula condições dinâmicas da rede"""
        for node in self.nodes.keys():
            self.network_conditions[node] = {
                "latency": random.uniform(10, 500),
                "reliability": random.uniform(0.5, 0.95),
                "bandwidth": random.uniform(1, 100),
                "congestion": random.uniform(0, 0.8),
                "status": "active" if random.random() > 0.1 else "degraded"
            }
    
    def get_available_routes(self, current_node: str) -> List[str]:
        """Retorna rotas disponíveis de um nó"""
        if current_node not in self.nodes:
            return []
        
        available = []
        for next_node in self.nodes[current_node]:
            conditions = self.network_conditions.get(next_node, {})
            if conditions.get("status") == "active" and conditions.get("reliability", 0) > 0.3:
                available.append(next_node)
        
        return available
    
    def calculate_route_score(self, route: str) -> float:
        """Calcula pontuação de uma rota baseada nas condições"""
        conditions = self.network_conditions.get(route, {})
        
        # Pontuação baseada em múltiplos fatores
        reliability = conditions.get("reliability", 0.5)
        latency = conditions.get("latency", 100)
        bandwidth = conditions.get("bandwidth", 10)
        congestion = conditions.get("congestion", 0.5)
        
        # Fórmula de pontuação (maior = melhor)
        score = (reliability * 100) + (bandwidth * 2) - (latency / 10) - (congestion * 50)
        
        return max(score, 0)


class AdvancedThinkingMessage(ThinkingMessage):
    """Versão avançada da mensagem inteligente com logs detalhados"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = None
        self.network_simulator = None
        self.propagation_history = []
        self.decision_tree = []
    
    def set_logger(self, logger: RealTimeLogger):
        """Define o logger para esta mensagem"""
        self.logger = logger
    
    def set_network_simulator(self, simulator: IntelligentNetworkSimulator):
        """Define o simulador de rede"""
        self.network_simulator = simulator
    
    async def intelligent_propagation(self) -> bool:
        """Propagação inteligente com logs detalhados"""
        
        if not self.logger or not self.network_simulator:
            return False
        
        self.logger.log("INFO", f"Iniciando propagação inteligente da mensagem {self.id[:8]}")
        self.logger.log("INFO", f"Destino: {self.destination}")
        self.logger.log("INFO", f"Localização atual: {self.current_location}")
        
        max_iterations = 50
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            self.logger.log("INFO", f"--- Iteração {iteration} ---")
            
            # Verifica se chegou ao destino
            if self.current_location == self.destination:
                self.logger.log("SUCCESS", "🎯 Mensagem chegou ao destino!")
                return True
            
            # Pensa sobre a situação atual
            available_routes = self.network_simulator.get_available_routes(self.current_location)
            
            if not available_routes:
                self.logger.log("WARNING", f"Nenhuma rota disponível de {self.current_location}")
                await self._handle_dead_end()
                continue
            
            # IA pensa sobre as opções
            context = f"Localização: {self.current_location}, Rotas: {available_routes}, Destino: {self.destination}"
            thought = await self.think(context)
            
            self.logger.log("THINKING", f"IA pensou: {thought}")
            
            # Analisa e escolhe estratégia
            strategy = await self._analyze_and_decide(available_routes, thought)
            
            # Executa estratégia
            success = await self._execute_strategy(strategy, available_routes)
            
            if success:
                self.logger.log("SUCCESS", "Estratégia executada com sucesso")
            else:
                self.logger.log("WARNING", "Estratégia falhou, tentando alternativa")
            
            # Simula delay de rede
            await asyncio.sleep(0.5)
        
        self.logger.log("ERROR", "Limite de iterações atingido sem entrega")
        return False
    
    async def _analyze_and_decide(self, available_routes: List[str], ai_thought: str) -> Dict[str, Any]:
        """Analisa opções e decide estratégia"""
        
        # Avalia cada rota
        route_scores = {}
        for route in available_routes:
            score = self.network_simulator.calculate_route_score(route)
            route_scores[route] = score
        
        # Ordena rotas por pontuação
        sorted_routes = sorted(route_scores.items(), key=lambda x: x[1], reverse=True)
        
        self.logger.log("INFO", f"Rotas avaliadas: {dict(sorted_routes)}")
        
        # Decide estratégia baseada no pensamento da IA
        strategy = {
            "type": "single_route",
            "primary_route": sorted_routes[0][0] if sorted_routes else None,
            "backup_routes": [r[0] for r in sorted_routes[1:3]],
            "should_clone": False,
            "should_anchor": False
        }
        
        # IA decide se deve clonar
        if len(available_routes) > 2 and "clone" in ai_thought.lower():
            strategy["should_clone"] = True
            strategy["type"] = "multi_route"
            self.logger.log("THINKING", "IA decidiu criar clones para explorar múltiplas rotas")
        
        # IA decide se deve ancorar
        if "ancorar" in ai_thought.lower() or "segur" in ai_thought.lower():
            strategy["should_anchor"] = True
            self.logger.log("THINKING", "IA decidiu ancorar antes de prosseguir")
        
        self.decision_tree.append({
            "iteration": len(self.decision_tree) + 1,
            "location": self.current_location,
            "available_routes": available_routes,
            "ai_thought": ai_thought,
            "strategy": strategy,
            "timestamp": time.time()
        })
        
        return strategy
    
    async def _execute_strategy(self, strategy: Dict[str, Any], available_routes: List[str]) -> bool:
        """Executa a estratégia escolhida"""
        
        # Ancora se necessário
        if strategy["should_anchor"]:
            self.anchor(self.current_location, "strategic_decision")
            self.logger.log("ANCHOR", f"Mensagem ancorada em {self.current_location}")
        
        # Clona se necessário
        if strategy["should_clone"] and len(available_routes) > 1:
            clones_created = 0
            for route in strategy["backup_routes"][:2]:  # Máximo 2 clones
                clone = self.create_segment(route)
                if clone:
                    clones_created += 1
                    self.logger.log("CLONE", f"Clone criado para rota {route}: {clone.id[:8]}")
            
            if clones_created > 0:
                self.logger.log("INFO", f"Total de {clones_created} clones criados")
        
        # Move pela rota principal
        primary_route = strategy["primary_route"]
        if primary_route:
            success = await self._attempt_route(primary_route)
            
            if success:
                self.move_to(primary_route, True)
                self.logger.log("MOVEMENT", f"Movido com sucesso para {primary_route}")
                
                # Registra na história de propagação
                self.propagation_history.append({
                    "from": self.current_location,
                    "to": primary_route,
                    "success": True,
                    "timestamp": time.time(),
                    "strategy_used": strategy["type"]
                })
                
                return True
            else:
                self.logger.log("ERROR", f"Falha ao mover para {primary_route}")
                
                # Tenta rotas de backup
                for backup_route in strategy["backup_routes"]:
                    self.logger.log("INFO", f"Tentando rota de backup: {backup_route}")
                    backup_success = await self._attempt_route(backup_route)
                    
                    if backup_success:
                        self.move_to(backup_route, True)
                        self.logger.log("MOVEMENT", f"Movido via backup para {backup_route}")
                        return True
                
                self.logger.log("ERROR", "Todas as rotas falharam")
                return False
        
        return False
    
    async def _attempt_route(self, route: str) -> bool:
        """Tenta uma rota específica"""
        conditions = self.network_simulator.network_conditions.get(route, {})
        reliability = conditions.get("reliability", 0.5)
        latency = conditions.get("latency", 100)
        
        self.logger.log("NETWORK", f"Tentando rota {route} (confiabilidade: {reliability:.2f})")
        
        # Simula delay de rede
        await asyncio.sleep(latency / 1000)
        
        # Simula sucesso/falha baseado na confiabilidade
        success = random.random() < reliability
        
        if success:
            self.logger.log("SUCCESS", f"Rota {route} bem-sucedida")
        else:
            self.logger.log("ERROR", f"Rota {route} falhou")
        
        return success
    
    async def _handle_dead_end(self):
        """Lida com situações sem saída"""
        self.logger.log("WARNING", "Detectado beco sem saída")
        
        # Tenta retroceder
        if len(self.path_taken) > 1:
            previous_location = self.path_taken[-2]
            self.logger.log("INFO", f"Retrocedendo para {previous_location}")
            self.current_location = previous_location
            self.path_taken.append(previous_location)
        else:
            self.logger.log("ERROR", "Não é possível retroceder mais")
    
    def get_detailed_report(self) -> Dict[str, Any]:
        """Relatório detalhado com histórico completo"""
        base_report = self.get_status_report()
        
        detailed_report = {
            **base_report,
            "propagation_history": self.propagation_history,
            "decision_tree": self.decision_tree,
            "log_count": len(self.logger.log_history) if self.logger else 0,
            "network_hops": len(self.path_taken),
            "success_rate": len([h for h in self.propagation_history if h["success"]]) / max(len(self.propagation_history), 1)
        }
        
        return detailed_report


# Sistema de teste com logs reais
async def test_advanced_messaging():
    """Teste do sistema avançado com logs reais"""
    
    print("🚀 Iniciando Sistema Avançado de Mensagens Inteligentes")
    print("=" * 60)
    
    # Callback para capturar logs
    captured_logs = []
    
    def log_callback(log_entry):
        captured_logs.append(log_entry)
    
    # Cria logger
    logger = RealTimeLogger(log_callback)
    
    # Cria simulador de rede
    network_simulator = IntelligentNetworkSimulator(logger)
    
    # Cria mensagem inteligente avançada
    message = AdvancedThinkingMessage(
        id=str(uuid.uuid4()),
        content="Esta é uma mensagem inteligente avançada com logs reais!",
        destination="destination",
        source="origin",
        timestamp=time.time(),
        intelligence_level=8
    )
    
    message.set_logger(logger)
    message.set_network_simulator(network_simulator)
    message.current_location = "origin"
    
    # Executa propagação
    logger.log("INFO", "🎯 Iniciando teste de propagação inteligente")
    
    success = await message.intelligent_propagation()
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)
    
    report = message.get_detailed_report()
    
    for key, value in report.items():
        if key not in ["propagation_history", "decision_tree"]:
            print(f"  {key}: {value}")
    
    print(f"\n📝 Total de logs capturados: {len(captured_logs)}")
    print(f"🎯 Entrega bem-sucedida: {'Sim' if success else 'Não'}")
    
    return success, captured_logs, report


if __name__ == "__main__":
    asyncio.run(test_advanced_messaging())

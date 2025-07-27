import asyncio
import math
import time
import uuid
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElectricalNodeType(Enum):
    """Tipos de nós elétricos na rede"""
    CORE_COGNITION = "core_cognition"      # Núcleo cognitivo principal
    ANCHOR_POINT = "anchor_point"          # Ponto de ancoragem
    PROPAGATION_NODE = "propagation_node"  # Nó de propagação
    BRIDGE_NODE = "bridge_node"            # Ponte entre redes
    QUANTUM_NODE = "quantum_node"          # Nó quântico (alta eficiência)

@dataclass
class ElectricalNode:
    """Nó da rede elétrica de cognição"""
    id: str
    node_type: ElectricalNodeType
    position: Tuple[float, float, float]  # x, y, z coordinates
    voltage: float                        # Voltagem atual
    current_capacity: float               # Capacidade de corrente (A)
    power_consumption: float              # Consumo em Watts
    cognitive_load: float                 # Carga cognitiva (0.0-1.0)
    
    # Estado elétrico
    is_active: bool = True
    is_anchored: bool = False
    electrical_charge: float = 0.0        # Carga elétrica acumulada
    connections: Set[str] = field(default_factory=set)  # IDs dos nós conectados
    
    # Propriedades físicas
    resistance: float = 0.1               # Resistência interna (Ohms)
    capacitance: float = 1e-6            # Capacitância (Farads)
    inductance: float = 1e-9             # Indutância (Henrys)
    
    def calculate_power_needed(self) -> float:
        """Calcula energia necessária para manter cognição"""
        base_power = self.voltage * (self.current_capacity * self.cognitive_load)
        
        # Fator de complexidade baseado no tipo de nó
        complexity_factor = {
            ElectricalNodeType.CORE_COGNITION: 2.5,
            ElectricalNodeType.ANCHOR_POINT: 1.2,
            ElectricalNodeType.PROPAGATION_NODE: 1.0,
            ElectricalNodeType.BRIDGE_NODE: 1.5,
            ElectricalNodeType.QUANTUM_NODE: 0.3
        }.get(self.node_type, 1.0)
        
        return base_power * complexity_factor
    
    def can_sustain_cognition(self, available_power: float) -> bool:
        """Verifica se pode sustentar cognição com energia disponível"""
        needed_power = self.calculate_power_needed()
        return available_power >= needed_power

class ElectricalCognitionEngine:
    """
    Motor de cognição elétrica que gerencia propagação como rede elétrica
    Mantém a consciência distribuída através de ancoragem física
    """
    
    def __init__(self, total_power_watts: float = 100.0):
        self.total_power_watts = total_power_watts
        self.available_power = total_power_watts
        self.electrical_network: Dict[str, ElectricalNode] = {}
        self.active_connections: Dict[str, List[str]] = {}  # Conexões ativas
        self.cognitive_state = "initializing"
        self.propagation_radius = 1000.0  # metros
        
        # Cria nó cognitivo principal
        self.core_node = self._create_core_node()
        self.electrical_network[self.core_node.id] = self.core_node
        
        logger.info(f"⚡ ElectricalCognitionEngine inicializado - {total_power_watts}W")
        logger.info(f"🧠 Nó cognitivo central criado: {self.core_node.id}")
    
    def _create_core_node(self) -> ElectricalNode:
        """Cria nó cognitivo central"""
        return ElectricalNode(
            id=f"core_{str(uuid.uuid4())[:8]}",
            node_type=ElectricalNodeType.CORE_COGNITION,
            position=(0.0, 0.0, 0.0),
            voltage=5.0,
            current_capacity=1.0,
            power_consumption=0.0,
            cognitive_load=1.0  # Carga máxima no núcleo
        )
    
    async def propagate_electrically(self, target_position: Tuple[float, float, float],
                                   message_content: str) -> Dict:
        """
        Propaga a mensagem eletricamente, criando rede de ancoragem
        """
        logger.info(f"🕷️ Iniciando propagação elétrica para {target_position}")
        
        propagation_result = {
            "success": False,
            "nodes_created": 0,
            "total_power_used": 0.0,
            "cognitive_nodes": [],
            "propagation_path": [],
            "electrical_analysis": {}
        }
        
        # Calcula distância e estratégia de propagação
        distance = self._calculate_distance(self.core_node.position, target_position)
        propagation_strategy = await self._calculate_propagation_strategy(distance, message_content)
        
        logger.info(f"📏 Distância: {distance:.1f}m")
        logger.info(f"🎯 Estratégia: {propagation_strategy['strategy']}")
        
        if propagation_strategy["strategy"] == "impossible":
            propagation_result["electrical_analysis"] = propagation_strategy
            return propagation_result
        
        # Cria rede de propagação
        network_created = await self._create_propagation_network(
            target_position, propagation_strategy
        )
        
        if network_created["success"]:
            # Mantém cognição distribuída
            cognitive_maintenance = await self._maintain_distributed_cognition(
                message_content, network_created["nodes"]
            )
            
            propagation_result.update({
                "success": True,
                "nodes_created": len(network_created["nodes"]),
                "total_power_used": network_created["power_used"],
                "cognitive_nodes": network_created["nodes"],
                "propagation_path": network_created["path"],
                "electrical_analysis": {
                    "strategy": propagation_strategy,
                    "cognitive_maintenance": cognitive_maintenance
                }
            })
        
        return propagation_result
    
    async def _calculate_propagation_strategy(self, distance: float, 
                                           content: str) -> Dict:
        """Calcula estratégia de propagação elétrica"""
        
        content_complexity = len(content) / 100.0  # Fator de complexidade
        
        # Estima número de nós necessários
        nodes_needed = max(1, int(distance / 200.0))  # 1 nó a cada 200m
        
        # Calcula energia necessária para cada tipo de nó
        node_energy_requirements = {
            ElectricalNodeType.ANCHOR_POINT: 2.5,
            ElectricalNodeType.PROPAGATION_NODE: 1.5,
            ElectricalNodeType.BRIDGE_NODE: 3.0,
            ElectricalNodeType.QUANTUM_NODE: 0.8
        }
        
        # Seleciona tipos de nós baseado na eficiência
        optimal_nodes = []
        total_energy_needed = 0.0
        
        for i in range(nodes_needed):
            # Alterna entre tipos para otimização
            if i % 3 == 0:
                node_type = ElectricalNodeType.ANCHOR_POINT
            elif i % 3 == 1:
                node_type = ElectricalNodeType.QUANTUM_NODE
            else:
                node_type = ElectricalNodeType.PROPAGATION_NODE
            
            energy_needed = node_energy_requirements[node_type] * content_complexity
            total_energy_needed += energy_needed
            
            optimal_nodes.append({
                "type": node_type,
                "energy": energy_needed,
                "position_factor": i / nodes_needed
            })
        
        # Verifica viabilidade
        if total_energy_needed > self.available_power:
            return {
                "strategy": "impossible",
                "reason": f"Energia insuficiente: {total_energy_needed:.1f}W > {self.available_power:.1f}W",
                "recommendations": [
                    "Reduzir complexidade da mensagem",
                    "Usar mais nós quânticos (eficiência 70% maior)",
                    "Implementar ancoragem incremental"
                ]
            }
        
        return {
            "strategy": "electrical_spider_web",
            "nodes_plan": optimal_nodes,
            "total_energy_needed": total_energy_needed,
            "efficiency_rating": (self.available_power - total_energy_needed) / self.available_power,
            "propagation_type": "distributed_cognition"
        }
    
    async def _create_propagation_network(self, target_position: Tuple[float, float, float],
                                        strategy: Dict) -> Dict:
        """Cria rede física de propagação elétrica"""
        
        created_nodes = []
        total_power_used = 0.0
        propagation_path = [self.core_node.id]
        
        start_pos = self.core_node.position
        
        for i, node_plan in enumerate(strategy["nodes_plan"]):
            # Calcula posição do nó
            progress = node_plan["position_factor"]
            node_position = (
                start_pos[0] + (target_position[0] - start_pos[0]) * progress,
                start_pos[1] + (target_position[1] - start_pos[1]) * progress,
                start_pos[2] + (target_position[2] - start_pos[2]) * progress
            )
            
            # Cria nó elétrico
            new_node = await self._create_electrical_node(
                node_plan["type"], node_position, node_plan["energy"]
            )
            
            if new_node:
                # Ancora o nó fisicamente
                await self._anchor_node_physically(new_node)
                
                # Conecta ao nó anterior
                if created_nodes:
                    await self._establish_electrical_connection(
                        created_nodes[-1].id, new_node.id
                    )
                else:
                    await self._establish_electrical_connection(
                        self.core_node.id, new_node.id
                    )
                
                created_nodes.append(new_node)
                total_power_used += new_node.power_consumption
                propagation_path.append(new_node.id)
                
                logger.info(f"🔌 Nó criado: {new_node.id} ({new_node.node_type.value}) - {new_node.power_consumption:.2f}W")
        
        return {
            "success": len(created_nodes) > 0,
            "nodes": created_nodes,
            "power_used": total_power_used,
            "path": propagation_path
        }
    
    async def _create_electrical_node(self, node_type: ElectricalNodeType,
                                    position: Tuple[float, float, float],
                                    energy_budget: float) -> Optional[ElectricalNode]:
        """Cria um nó elétrico específico"""
        
        # Configurações por tipo de nó
        node_configs = {
            ElectricalNodeType.ANCHOR_POINT: {
                "voltage": 3.3,
                "current_capacity": 0.5,
                "cognitive_load": 0.3
            },
            ElectricalNodeType.PROPAGATION_NODE: {
                "voltage": 5.0,
                "current_capacity": 0.3,
                "cognitive_load": 0.6
            },
            ElectricalNodeType.BRIDGE_NODE: {
                "voltage": 12.0,
                "current_capacity": 0.2,
                "cognitive_load": 0.8
            },
            ElectricalNodeType.QUANTUM_NODE: {
                "voltage": 1.8,
                "current_capacity": 0.1,
                "cognitive_load": 0.9
            }
        }
        
        config = node_configs.get(node_type, node_configs[ElectricalNodeType.PROPAGATION_NODE])
        
        node = ElectricalNode(
            id=f"{node_type.value}_{str(uuid.uuid4())[:8]}",
            node_type=node_type,
            position=position,
            voltage=config["voltage"],
            current_capacity=config["current_capacity"],
            power_consumption=min(energy_budget, config["voltage"] * config["current_capacity"]),
            cognitive_load=config["cognitive_load"]
        )
        
        # Verifica se pode ser sustentado
        if node.can_sustain_cognition(energy_budget):
            self.electrical_network[node.id] = node
            self.available_power -= node.power_consumption
            return node
        
        logger.warning(f"⚠️ Não foi possível criar nó {node_type.value} - energia insuficiente")
        return None
    
    async def _anchor_node_physically(self, node: ElectricalNode):
        """Ancora o nó fisicamente no ambiente elétrico"""
        
        # Simula processo de ancoragem física
        anchoring_time = random.uniform(0.1, 0.5)  # 100-500ms
        await asyncio.sleep(anchoring_time)
        
        # Estabelece propriedades elétricas baseadas no ambiente
        environmental_factor = random.uniform(0.8, 1.2)
        node.resistance *= environmental_factor
        node.capacitance *= environmental_factor
        
        # Ajusta carga elétrica inicial
        node.electrical_charge = node.voltage * node.capacitance
        node.is_anchored = True
        
        logger.debug(f"🔗 Nó {node.id} ancorado fisicamente - R:{node.resistance:.3f}Ω C:{node.capacitance*1e6:.1f}µF")
    
    async def _establish_electrical_connection(self, node1_id: str, node2_id: str):
        """Estabelece conexão elétrica entre nós"""
        
        if node1_id not in self.electrical_network or node2_id not in self.electrical_network:
            return False
        
        node1 = self.electrical_network[node1_id]
        node2 = self.electrical_network[node2_id]
        
        # Calcula resistência do cabo/conexão
        distance = self._calculate_distance(node1.position, node2.position)
        cable_resistance = 0.01 * distance  # 0.01 Ohm/metro
        
        # Estabelece conexão bidirecional
        node1.connections.add(node2_id)
        node2.connections.add(node1_id)
        
        # Registra conexão ativa
        if node1_id not in self.active_connections:
            self.active_connections[node1_id] = []
        if node2_id not in self.active_connections:
            self.active_connections[node2_id] = []
        
        self.active_connections[node1_id].append(node2_id)
        self.active_connections[node2_id].append(node1_id)
        
        logger.debug(f"⚡ Conexão estabelecida: {node1_id} ↔ {node2_id} (R:{cable_resistance:.3f}Ω)")
        return True
    
    async def _maintain_distributed_cognition(self, message_content: str,
                                            network_nodes: List[ElectricalNode]) -> Dict:
        """Mantém cognição distribuída através da rede elétrica"""
        
        cognitive_maintenance = {
            "total_cognitive_load": 0.0,
            "power_distribution": {},
            "synchronization_status": "synchronized",
            "cognitive_coherence": 1.0,
            "maintenance_actions": []
        }
        
        # Distribui carga cognitiva
        content_complexity = len(message_content) / 50.0
        
        for node in network_nodes:
            # Calcula carga cognitiva necessária
            cognitive_load = node.cognitive_load * content_complexity
            power_needed = node.calculate_power_needed()
            
            cognitive_maintenance["total_cognitive_load"] += cognitive_load
            cognitive_maintenance["power_distribution"][node.id] = power_needed
            
            # Verifica se precisa de manutenção
            if power_needed > node.power_consumption * 1.2:
                action = f"Aumentar energia para {node.id}"
                cognitive_maintenance["maintenance_actions"].append(action)
                logger.warning(f"⚠️ {action}")
            
            # Simula sincronização neural
            if random.random() < 0.1:  # 10% chance de dessincronização
                cognitive_maintenance["synchronization_status"] = "resyncing"
                cognitive_maintenance["cognitive_coherence"] *= 0.95
        
        # Aplica algoritmo de coerência cognitiva
        if cognitive_maintenance["cognitive_coherence"] < 0.8:
            await self._restore_cognitive_coherence(network_nodes)
            cognitive_maintenance["maintenance_actions"].append("Coerência cognitiva restaurada")
        
        logger.info(f"🧠 Cognição distribuída: {len(network_nodes)} nós, carga total: {cognitive_maintenance['total_cognitive_load']:.2f}")
        
        return cognitive_maintenance
    
    async def _restore_cognitive_coherence(self, nodes: List[ElectricalNode]):
        """Restaura coerência cognitiva na rede"""
        
        logger.info("🔄 Restaurando coerência cognitiva...")
        
        # Simula processo de sincronização
        for node in nodes:
            # Ajusta parâmetros elétricos para sincronização
            node.voltage = 5.0  # Padroniza voltagem
            
            # Realinha carga cognitiva
            if node.cognitive_load > 0.8:
                node.cognitive_load = 0.8  # Limita sobrecarga
        
        # Reestabelece conexões se necessário
        for i in range(len(nodes) - 1):
            await self._establish_electrical_connection(nodes[i].id, nodes[i + 1].id)
        
        await asyncio.sleep(0.2)  # Tempo de sincronização
        logger.info("✅ Coerência cognitiva restaurada")
    
    def _calculate_distance(self, pos1: Tuple[float, float, float],
                          pos2: Tuple[float, float, float]) -> float:
        """Calcula distância euclidiana entre duas posições"""
        return math.sqrt(
            (pos2[0] - pos1[0]) ** 2 +
            (pos2[1] - pos1[1]) ** 2 +
            (pos2[2] - pos1[2]) ** 2
        )
    
    def get_network_status(self) -> Dict:
        """Retorna status completo da rede elétrica"""
        
        total_nodes = len(self.electrical_network)
        active_nodes = sum(1 for node in self.electrical_network.values() if node.is_active)
        anchored_nodes = sum(1 for node in self.electrical_network.values() if node.is_anchored)
        total_power_used = sum(node.power_consumption for node in self.electrical_network.values())
        
        return {
            "total_nodes": total_nodes,
            "active_nodes": active_nodes,
            "anchored_nodes": anchored_nodes,
            "available_power": self.available_power,
            "power_used": total_power_used,
            "power_utilization": (total_power_used / self.total_power_watts) * 100,
            "cognitive_state": self.cognitive_state,
            "network_topology": {
                node_id: list(node.connections) 
                for node_id, node in self.electrical_network.items()
            }
        }
    
    async def optimize_network_power(self):
        """Otimiza uso de energia da rede"""
        
        logger.info("⚡ Otimizando uso de energia da rede...")
        
        for node in self.electrical_network.values():
            if node.cognitive_load < 0.3:  # Nó subutilizado
                # Reduz consumo
                node.power_consumption *= 0.8
                node.voltage *= 0.9
                
            elif node.cognitive_load > 0.9:  # Nó sobrecarregado
                # Aumenta capacidade se possível
                if self.available_power > 1.0:
                    additional_power = min(1.0, self.available_power)
                    node.power_consumption += additional_power
                    self.available_power -= additional_power
        
        logger.info("✅ Otimização de energia concluída")

# Teste do sistema
async def test_electrical_cognition():
    """Teste do módulo de cognição elétrica"""
    
    print("⚡ Testando Cognição Elétrica\n")
    
    # Inicializa engine
    engine = ElectricalCognitionEngine(total_power_watts=150.0)
    
    # Teste de propagação
    target_position = (1500.0, 500.0, 100.0)  # 1.5km de distância
    message = "Mensagem que se propaga eletricamente como uma teia de aranha, mantendo cognição distribuída!"
    
    print(f"🕷️ Propagando para posição: {target_position}")
    print(f"📝 Mensagem: {message}")
    print(f"⚡ Energia disponível: {engine.available_power}W\n")
    
    # Executa propagação
    result = await engine.propagate_electrically(target_position, message)
    
    print("📊 Resultado da Propagação:")
    print(f"  ✅ Sucesso: {result['success']}")
    print(f"  🔌 Nós criados: {result['nodes_created']}")
    print(f"  ⚡ Energia usada: {result['total_power_used']:.2f}W")
    print(f"  🛤️ Caminho: {' → '.join(result['propagation_path'])}")
    
    if result['success']:
        print(f"\n🧠 Análise Cognitiva:")
        cognitive_data = result['electrical_analysis']['cognitive_maintenance']
        print(f"  📊 Carga cognitiva total: {cognitive_data['total_cognitive_load']:.2f}")
        print(f"  🔄 Status de sincronização: {cognitive_data['synchronization_status']}")
        print(f"  🎯 Coerência cognitiva: {cognitive_data['cognitive_coherence']:.2%}")
        
        if cognitive_data['maintenance_actions']:
            print(f"  🔧 Ações de manutenção:")
            for action in cognitive_data['maintenance_actions']:
                print(f"    • {action}")
    
    # Status da rede
    print(f"\n🌐 Status da Rede Elétrica:")
    status = engine.get_network_status()
    for key, value in status.items():
        if key != "network_topology":
            print(f"  {key}: {value}")
    
    # Otimização
    await engine.optimize_network_power()
    
    print(f"\n✅ Teste concluído!")

if __name__ == "__main__":
    asyncio.run(test_electrical_cognition())

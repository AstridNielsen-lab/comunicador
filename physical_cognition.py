import asyncio
import math
import time
import uuid
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransmissionMedium(Enum):
    COPPER_WIRE = "copper_wire"
    FIBER_OPTIC = "fiber_optic"
    RADIO_WAVE = "radio_wave"
    BLUETOOTH = "bluetooth"
    WIFI = "wifi"
    CELLULAR = "cellular"
    ACOUSTIC = "acoustic"
    LIGHT_BEAM = "light_beam"

@dataclass
class PhysicalProperties:
    """Propriedades físicas do meio de transmissão"""
    resistance_per_meter: float  # Ohms/metro
    attenuation_db_per_meter: float  # dB/metro
    max_frequency: float  # Hz
    propagation_speed: float  # m/s
    energy_efficiency: float  # 0.0 - 1.0
    medium_type: TransmissionMedium

@dataclass
class PulseConfiguration:
    """Configuração de um pulso elétrico"""
    voltage: float  # Volts
    current: float  # Amperes
    duration: float  # segundos
    frequency: float  # Hz (pulsos por segundo)
    
    def energy_per_pulse(self) -> float:
        """Calcula energia por pulso em Joules"""
        return self.voltage * self.current * self.duration
    
    def power_consumption(self) -> float:
        """Calcula consumo de energia em Watts"""
        return self.energy_per_pulse() * self.frequency

class PhysicalCognitionEngine:
    """
    Módulo de cognição física que pensa em termos de energia,
    voltagem, resistência e eficiência para otimizar transmissão
    """
    
    def __init__(self, max_power_watts: float = 100.0):
        self.max_power_watts = max_power_watts
        self.current_power_usage = 0.0
        
        # Base de conhecimento dos meios físicos
        self.medium_properties = {
            TransmissionMedium.COPPER_WIRE: PhysicalProperties(
                resistance_per_meter=0.017,  # Ohms/m (cobre)
                attenuation_db_per_meter=0.01,
                max_frequency=1e9,  # 1 GHz
                propagation_speed=2.1e8,  # 70% velocidade da luz
                energy_efficiency=0.85,
                medium_type=TransmissionMedium.COPPER_WIRE
            ),
            TransmissionMedium.WIFI: PhysicalProperties(
                resistance_per_meter=0.0,  # Sem fio
                attenuation_db_per_meter=0.1,  # Atenuação do ar
                max_frequency=5.8e9,  # 5.8 GHz
                propagation_speed=3e8,  # Velocidade da luz
                energy_efficiency=0.60,
                medium_type=TransmissionMedium.WIFI
            ),
            TransmissionMedium.CELLULAR: PhysicalProperties(
                resistance_per_meter=0.0,
                attenuation_db_per_meter=0.05,
                max_frequency=3.5e9,  # 5G
                propagation_speed=3e8,
                energy_efficiency=0.50,
                medium_type=TransmissionMedium.CELLULAR
            ),
            TransmissionMedium.BLUETOOTH: PhysicalProperties(
                resistance_per_meter=0.0,
                attenuation_db_per_meter=0.2,
                max_frequency=2.4e9,
                propagation_speed=3e8,
                energy_efficiency=0.75,
                medium_type=TransmissionMedium.BLUETOOTH
            ),
            TransmissionMedium.FIBER_OPTIC: PhysicalProperties(
                resistance_per_meter=0.0,  # Fibra óptica
                attenuation_db_per_meter=0.0002,  # Muito baixa
                max_frequency=1e15,  # Luz infravermelha
                propagation_speed=2e8,  # 67% velocidade da luz
                energy_efficiency=0.95,
                medium_type=TransmissionMedium.FIBER_OPTIC
            ),
            TransmissionMedium.RADIO_WAVE: PhysicalProperties(
                resistance_per_meter=0.0,  # Sem fio
                attenuation_db_per_meter=0.08,  # Atenuação moderada
                max_frequency=900e6,  # 900 MHz (LoRa típico)
                propagation_speed=3e8,  # Velocidade da luz
                energy_efficiency=0.65,
                medium_type=TransmissionMedium.RADIO_WAVE
            ),
            TransmissionMedium.ACOUSTIC: PhysicalProperties(
                resistance_per_meter=0.0,  # Ondas sonoras
                attenuation_db_per_meter=2.0,  # Alta atenuação no ar
                max_frequency=20000,  # 20 kHz (limite audível)
                propagation_speed=343,  # Velocidade do som no ar
                energy_efficiency=0.30,
                medium_type=TransmissionMedium.ACOUSTIC
            ),
            TransmissionMedium.LIGHT_BEAM: PhysicalProperties(
                resistance_per_meter=0.0,  # Feixe de luz
                attenuation_db_per_meter=0.5,  # Atenuação por partículas no ar
                max_frequency=5e14,  # Luz visível
                propagation_speed=3e8,  # Velocidade da luz
                energy_efficiency=0.80,
                medium_type=TransmissionMedium.LIGHT_BEAM
            )
        }
        
        logger.info(f"🧠 PhysicalCognitionEngine inicializado - Limite: {max_power_watts}W")
    
    async def analyze_transmission_challenge(self, destination: str, 
                                           message_size_bytes: int,
                                           available_media: List[TransmissionMedium],
                                           estimated_distance: float = 1000.0) -> Dict:
        """
        Analisa o desafio de transmissão usando cognição física
        """
        logger.info(f"🔬 Analisando transmissão: {message_size_bytes} bytes para {destination}")
        logger.info(f"📏 Distância estimada: {estimated_distance}m")
        logger.info(f"🌐 Meios disponíveis: {len(available_media)}")
        
        analysis = {
            "destination": destination,
            "message_size_bytes": message_size_bytes,
            "distance_meters": estimated_distance,
            "available_power_watts": self.max_power_watts - self.current_power_usage,
            "medium_analysis": [],
            "recommended_strategy": None,
            "energy_calculations": {},
            "physical_constraints": {}
        }
        
        # Analisa cada meio disponível
        for medium in available_media:
            medium_analysis = await self._analyze_medium(medium, estimated_distance, message_size_bytes)
            analysis["medium_analysis"].append(medium_analysis)
        
        # Calcula estratégia ótima
        strategy = await self._calculate_optimal_strategy(analysis)
        analysis["recommended_strategy"] = strategy
        
        # Reflexões cognitivas da IA
        reflections = await self._generate_physical_reflections(analysis)
        analysis["ai_reflections"] = reflections
        
        return analysis
    
    async def _analyze_medium(self, medium: TransmissionMedium, 
                            distance: float, message_size: int) -> Dict:
        """Analisa um meio específico usando física"""
        
        properties = self.medium_properties[medium]
        
        # Calcula bits necessários
        bits_to_transmit = message_size * 8
        
        # Configuração de pulso otimizada para este meio
        pulse_config = self._optimize_pulse_for_medium(medium, distance)
        
        # Calcula perdas por distância
        if medium in [TransmissionMedium.COPPER_WIRE]:
            # Perdas resistivas em condutores
            total_resistance = properties.resistance_per_meter * distance
            power_loss = pulse_config.current ** 2 * total_resistance
        else:
            # Perdas por atenuação em meios sem fio
            power_loss = self._calculate_wireless_attenuation(properties, distance)
        
        # Tempo de transmissão
        transmission_time = bits_to_transmit / pulse_config.frequency
        
        # Energia total necessária
        base_energy = pulse_config.power_consumption() * transmission_time
        total_energy_with_losses = base_energy * (1 + power_loss / base_energy)
        
        return {
            "medium": medium.value,
            "properties": properties,
            "pulse_config": pulse_config,
            "transmission_time_seconds": transmission_time,
            "base_energy_joules": base_energy,
            "power_loss_watts": power_loss,
            "total_energy_required_joules": total_energy_with_losses,
            "efficiency": properties.energy_efficiency,
            "feasible": total_energy_with_losses <= self.max_power_watts * transmission_time,
            "quality_score": self._calculate_quality_score(properties, pulse_config, power_loss)
        }
    
    def _optimize_pulse_for_medium(self, medium: TransmissionMedium, distance: float) -> PulseConfiguration:
        """Otimiza configuração de pulso para um meio específico"""
        
        properties = self.medium_properties[medium]
        
        # Configurações base por tipo de meio
        if medium == TransmissionMedium.COPPER_WIRE:
            # Para cobre: voltagem maior para superar resistência
            base_voltage = 5.0 + (distance / 1000) * 2.0  # Aumenta com distância
            base_current = 0.02  # 20mA
            pulse_duration = 0.001  # 1ms
            frequency = min(1e6, properties.max_frequency * 0.1)  # 1MHz ou 10% do máximo
            
        elif medium == TransmissionMedium.WIFI:
            # WiFi: pulsos mais rápidos, menor duração
            base_voltage = 3.3
            base_current = 0.015
            pulse_duration = 0.0001  # 100µs
            frequency = 10e6  # 10MHz
            
        elif medium == TransmissionMedium.CELLULAR:
            # Celular: otimizado para longa distância
            base_voltage = 3.7
            base_current = 0.025
            pulse_duration = 0.0005  # 500µs
            frequency = 2e6  # 2MHz
            
        elif medium == TransmissionMedium.BLUETOOTH:
            # Bluetooth: baixo consumo
            base_voltage = 1.8
            base_current = 0.008
            pulse_duration = 0.001  # 1ms
            frequency = 1e6  # 1MHz
            
        else:
            # Configuração padrão
            base_voltage = 3.3
            base_current = 0.01
            pulse_duration = 0.001
            frequency = 1e6
        
        return PulseConfiguration(
            voltage=base_voltage,
            current=base_current,
            duration=pulse_duration,
            frequency=frequency
        )
    
    def _calculate_wireless_attenuation(self, properties: PhysicalProperties, distance: float) -> float:
        """Calcula atenuação para meios sem fio"""
        # Lei do quadrado inverso + atenuação do meio
        free_space_loss_db = 20 * math.log10(distance) + 20 * math.log10(properties.max_frequency) - 147.55
        medium_loss_db = properties.attenuation_db_per_meter * distance
        total_loss_db = free_space_loss_db + medium_loss_db
        
        # Converte dB para fator linear
        loss_factor = 10 ** (total_loss_db / 10)
        return loss_factor
    
    def _calculate_quality_score(self, properties: PhysicalProperties, 
                               pulse_config: PulseConfiguration, power_loss: float) -> float:
        """Calcula score de qualidade do meio"""
        efficiency_score = properties.energy_efficiency
        power_score = 1.0 / (1.0 + power_loss / 10.0)  # Penaliza perdas altas
        frequency_score = min(1.0, pulse_config.frequency / 1e6)  # Favorece frequências altas
        
        return (efficiency_score * 0.5 + power_score * 0.3 + frequency_score * 0.2)
    
    async def _calculate_optimal_strategy(self, analysis: Dict) -> Dict:
        """Calcula estratégia ótima usando cognição física"""
        
        # Ordena meios por qualidade
        media_by_quality = sorted(
            analysis["medium_analysis"],
            key=lambda x: x["quality_score"],
            reverse=True
        )
        
        feasible_media = [m for m in media_by_quality if m["feasible"]]
        
        if not feasible_media:
            return {
                "strategy": "impossible",
                "reason": "Nenhum meio viável com energia disponível",
                "recommendations": [
                    "Reduzir tamanho da mensagem",
                    "Aumentar limite de energia",
                    "Usar repetidores"
                ]
            }
        
        best_medium = feasible_media[0]
        
        strategy = {
            "strategy": "single_medium",
            "selected_medium": best_medium["medium"],
            "energy_required_joules": best_medium["total_energy_required_joules"],
            "transmission_time_seconds": best_medium["transmission_time_seconds"],
            "efficiency": best_medium["efficiency"],
            "pulse_configuration": best_medium["pulse_config"]
        }
        
        # Verifica se vale a pena usar múltiplos meios
        if len(feasible_media) > 1:
            multi_strategy = await self._analyze_multi_medium_strategy(feasible_media)
            if multi_strategy["total_efficiency"] > best_medium["efficiency"]:
                strategy = multi_strategy
        
        return strategy
    
    async def _analyze_multi_medium_strategy(self, feasible_media: List[Dict]) -> Dict:
        """Analisa estratégia usando múltiplos meios simultaneamente"""
        
        # Divide a mensagem entre os meios mais eficientes
        total_energy = sum(m["total_energy_required_joules"] for m in feasible_media[:3])
        total_time = max(m["transmission_time_seconds"] for m in feasible_media[:3])
        total_efficiency = sum(m["efficiency"] for m in feasible_media[:3]) / len(feasible_media[:3])
        
        return {
            "strategy": "multi_medium",
            "selected_media": [m["medium"] for m in feasible_media[:3]],
            "total_energy_joules": total_energy,
            "total_time_seconds": total_time,
            "total_efficiency": total_efficiency,
            "medium_distribution": {
                m["medium"]: f"{100/len(feasible_media[:3]):.1f}%" 
                for m in feasible_media[:3]
            }
        }
    
    async def _generate_physical_reflections(self, analysis: Dict) -> List[str]:
        """Gera reflexões cognitivas baseadas em física"""
        
        reflections = []
        
        total_power_needed = sum(
            m.get("total_energy_required_joules", 0) / m.get("transmission_time_seconds", 1)
            for m in analysis["medium_analysis"] if m.get("feasible", False)
        )
        
        power_utilization = total_power_needed / self.max_power_watts
        
        # Reflexões sobre energia
        if power_utilization > 0.8:
            reflections.append(
                f"⚡ Alto consumo energético detectado ({power_utilization:.1%}). "
                f"Preciso otimizar pulsos para reduzir desperdício de energia."
            )
        
        # Reflexões sobre eficiência
        best_efficiency = max(
            (m.get("efficiency", 0) for m in analysis["medium_analysis"]), 
            default=0
        )
        if best_efficiency < 0.7:
            reflections.append(
                f"🔧 Eficiência baixa ({best_efficiency:.1%}). Vou ajustar voltagem e "
                f"corrente para minimizar perdas por resistência."
            )
        
        # Reflexões sobre distância
        distance = analysis["distance_meters"]
        if distance > 5000:
            reflections.append(
                f"📡 Distância longa ({distance}m) detectada. Considerando uso de "
                f"repetidores ou aumento de potência para superar atenuação."
            )
        
        # Reflexões sobre meio físico
        copper_media = [m for m in analysis["medium_analysis"] 
                       if m.get("medium") == "copper_wire"]
        if copper_media:
            resistance_loss = copper_media[0].get("power_loss_watts", 0)
            if resistance_loss > 10:
                reflections.append(
                    f"⚙️ Perdas resistivas altas ({resistance_loss:.1f}W) em cobre. "
                    f"Vou aumentar a seção do condutor ou usar voltagem maior."
                )
        
        # Reflexões sobre frequência
        wireless_media = [m for m in analysis["medium_analysis"] 
                         if m.get("medium") in ["wifi", "cellular", "bluetooth"]]
        if wireless_media:
            avg_freq = sum(m["pulse_config"].frequency for m in wireless_media) / len(wireless_media)
            if avg_freq > 5e9:
                reflections.append(
                    f"📶 Frequência alta ({avg_freq/1e9:.1f}GHz) pode causar interferência. "
                    f"Vou usar técnicas de espalhamento espectral."
                )
        
        # Reflexão final sobre estratégia
        strategy = analysis.get("recommended_strategy", {})
        if strategy.get("strategy") == "multi_medium":
            reflections.append(
                f"🔀 Estratégia multi-meio selecionada para maximizar robustez e "
                f"distribuir carga energética entre diferentes canais físicos."
            )
        
        return reflections

# Exemplo de uso integrado com o sistema existente
class PhysicallyAwareMessage:
    """Mensagem com consciência física para otimização de transmissão"""
    
    def __init__(self, content: str, destination: str, 
                 physical_engine: PhysicalCognitionEngine):
        self.id = str(uuid.uuid4())
        self.content = content
        self.destination = destination
        self.physical_engine = physical_engine
        self.size_bytes = len(content.encode('utf-8'))
        self.transmission_analysis = None
        
    async def analyze_physical_constraints(self, available_media: List[TransmissionMedium],
                                         estimated_distance: float = 1000.0):
        """Analisa restrições físicas para esta mensagem"""
        
        self.transmission_analysis = await self.physical_engine.analyze_transmission_challenge(
            destination=self.destination,
            message_size_bytes=self.size_bytes,
            available_media=available_media,
            estimated_distance=estimated_distance
        )
        
        logger.info(f"📊 Análise física completa para mensagem {self.id[:8]}")
        return self.transmission_analysis
    
    async def adapt_transmission_strategy(self):
        """Adapta estratégia baseada na análise física"""
        
        if not self.transmission_analysis:
            logger.warning("⚠️ Análise física não realizada")
            return False
        
        strategy = self.transmission_analysis["recommended_strategy"]
        
        if strategy["strategy"] == "impossible":
            logger.error(f"❌ Transmissão impossível: {strategy['reason']}")
            logger.info(f"💡 Recomendações: {', '.join(strategy['recommendations'])}")
            return False
        
        logger.info(f"✅ Estratégia selecionada: {strategy['strategy']}")
        
        if strategy["strategy"] == "single_medium":
            logger.info(f"🎯 Meio selecionado: {strategy['selected_medium']}")
            logger.info(f"⚡ Energia necessária: {strategy['energy_required_joules']:.3f}J")
            logger.info(f"⏱️ Tempo de transmissão: {strategy['transmission_time_seconds']:.3f}s")
            
        elif strategy["strategy"] == "multi_medium":
            logger.info(f"🔀 Meios múltiplos: {', '.join(strategy['selected_media'])}")
            logger.info(f"📊 Distribuição: {strategy['medium_distribution']}")
        
        return True
    
    def get_physical_reflections(self) -> List[str]:
        """Retorna reflexões da IA sobre física da transmissão"""
        if self.transmission_analysis:
            return self.transmission_analysis.get("ai_reflections", [])
        return []

# Teste do sistema
async def test_physical_cognition():
    """Teste do módulo de cognição física"""
    
    print("🧠 Testando Módulo de Cognição Física\n")
    
    # Inicializa engine
    engine = PhysicalCognitionEngine(max_power_watts=100.0)
    
    # Cria mensagem
    message = PhysicallyAwareMessage(
        content="Esta é uma mensagem que precisa ser transmitida usando cognição física!",
        destination="servidor_remoto",
        physical_engine=engine
    )
    
    # Meios disponíveis
    available_media = [
        TransmissionMedium.WIFI,
        TransmissionMedium.CELLULAR,
        TransmissionMedium.BLUETOOTH,
        TransmissionMedium.COPPER_WIRE
    ]
    
    print(f"📝 Mensagem: {message.content}")
    print(f"📏 Tamanho: {message.size_bytes} bytes")
    print(f"🎯 Destino: {message.destination}")
    print(f"🌐 Meios disponíveis: {[m.value for m in available_media]}\n")
    
    # Analisa restrições físicas
    await message.analyze_physical_constraints(
        available_media=available_media,
        estimated_distance=1500.0  # 1.5km
    )
    
    # Adapta estratégia
    success = await message.adapt_transmission_strategy()
    
    print(f"\n🤔 Reflexões da IA:")
    for reflection in message.get_physical_reflections():
        print(f"  {reflection}")
    
    print(f"\n✅ Sucesso: {success}")

if __name__ == "__main__":
    asyncio.run(test_physical_cognition())

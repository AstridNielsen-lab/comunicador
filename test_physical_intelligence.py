#!/usr/bin/env python3
"""
Teste completo do sistema de mensagens inteligentes com cognição física
"""

import asyncio
import time
from intelligent_message import ThinkingMessage
from physical_cognition import PhysicalCognitionEngine, TransmissionMedium

async def test_complete_system():
    """Teste completo do sistema integrado"""
    
    print("=" * 60)
    print("🧠 TESTE DO SISTEMA DE COGNIÇÃO FÍSICA")
    print("=" * 60)
    
    # === CENÁRIO 1: Mensagem com poucos recursos ===
    print("\n📋 CENÁRIO 1: Mensagem com recursos limitados")
    print("-" * 40)
    
    limited_message = ThinkingMessage(
        id="msg_limited_001",
        content="Mensagem urgente que precisa chegar ao destino com poucos recursos!",
        destination="servidor_emergencia",
        source="dispositivo_remoto",
        timestamp=time.time(),
        available_power_watts=50.0,  # Apenas 50W disponíveis
        intelligence_level=8
    )
    
    print(f"📝 Conteúdo: {limited_message.content}")
    print(f"⚡ Energia disponível: {limited_message.available_power_watts}W")
    print(f"🧠 Nível de inteligência: {limited_message.intelligence_level}")
    
    # Redes disponíveis (limitadas)
    limited_networks = ["bluetooth", "lora"]
    
    print(f"🌐 Redes disponíveis: {limited_networks}")
    
    # Executa um ciclo de propagação
    print("\n🚀 Iniciando propagação...")
    await limited_message.autonomous_propagation(limited_networks)
    
    # === CENÁRIO 2: Mensagem com muitos recursos ===
    print("\n" + "=" * 60)
    print("📋 CENÁRIO 2: Mensagem com recursos abundantes")
    print("-" * 40)
    
    rich_message = ThinkingMessage(
        id="msg_rich_001",
        content="Transmissão de dados importantes com recursos abundantes para garantir entrega.",
        destination="data_center_principal",
        source="estacao_base",
        timestamp=time.time(),
        available_power_watts=200.0,  # 200W disponíveis
        intelligence_level=10
    )
    
    print(f"📝 Conteúdo: {rich_message.content}")
    print(f"⚡ Energia disponível: {rich_message.available_power_watts}W")
    print(f"🧠 Nível de inteligência: {rich_message.intelligence_level}")
    
    # Redes disponíveis (muitas opções)
    rich_networks = ["wifi", "cellular", "fiber", "ethernet", "bluetooth"]
    
    print(f"🌐 Redes disponíveis: {rich_networks}")
    
    # Executa um ciclo de propagação
    print("\n🚀 Iniciando propagação...")
    await rich_message.autonomous_propagation(rich_networks)
    
    # === CENÁRIO 3: Longa distância ===
    print("\n" + "=" * 60)
    print("📋 CENÁRIO 3: Transmissão de longa distância")
    print("-" * 40)
    
    long_distance_message = ThinkingMessage(
        id="msg_long_001",
        content="Mensagem que precisa percorrer uma grande distância.",
        destination="satelite_orbital",
        source="estacao_terrestre",
        timestamp=time.time(),
        available_power_watts=150.0,
        intelligence_level=9
    )
    
    # Simula que já teve várias falhas (indica distância longa)
    long_distance_message.memory["failed_attempts"] = [
        {"from": "terra", "to": "atmosfera", "timestamp": time.time() - 100, "success": False},
        {"from": "atmosfera", "to": "espaco", "timestamp": time.time() - 50, "success": False},
    ]
    
    print(f"📝 Conteúdo: {long_distance_message.content}")
    print(f"⚡ Energia disponível: {long_distance_message.available_power_watts}W")
    print(f"❌ Falhas anteriores: {len(long_distance_message.memory['failed_attempts'])}")
    
    # Redes especializadas para longa distância
    long_distance_networks = ["cellular", "radio_wave", "fiber"]
    
    print(f"🌐 Redes disponíveis: {long_distance_networks}")
    
    # Executa um ciclo de propagação
    print("\n🚀 Iniciando propagação...")
    await long_distance_message.autonomous_propagation(long_distance_networks)
    
    # === ANÁLISE COMPARATIVA ===
    print("\n" + "=" * 60)
    print("📊 ANÁLISE COMPARATIVA DOS CENÁRIOS")
    print("-" * 40)
    
    messages = [
        ("Recursos Limitados", limited_message),
        ("Recursos Abundantes", rich_message),
        ("Longa Distância", long_distance_message)
    ]
    
    for scenario_name, message in messages:
        print(f"\n🔍 {scenario_name}:")
        
        if message.physical_analysis:
            strategy = message.physical_analysis["recommended_strategy"]
            
            print(f"  📋 Estratégia: {strategy.get('strategy', 'N/A')}")
            
            if strategy.get("strategy") == "single_medium":
                print(f"  🌐 Meio selecionado: {strategy.get('selected_medium', 'N/A')}")
                print(f"  ⚡ Energia necessária: {strategy.get('energy_required_joules', 0):.3f}J")
                print(f"  ⏱️ Tempo estimado: {strategy.get('transmission_time_seconds', 0):.3f}s")
                print(f"  📈 Eficiência: {strategy.get('efficiency', 0):.1%}")
                
            elif strategy.get("strategy") == "multi_medium":
                print(f"  🔀 Múltiplos meios: {', '.join(strategy.get('selected_media', []))}")
                print(f"  ⚡ Energia total: {strategy.get('total_energy_joules', 0):.3f}J")
                print(f"  📈 Eficiência total: {strategy.get('total_efficiency', 0):.1%}")
                
            elif strategy.get("strategy") == "impossible":
                print(f"  ❌ Impossível: {strategy.get('reason', 'N/A')}")
                print(f"  💡 Recomendações: {', '.join(strategy.get('recommendations', []))}")
        
        # Reflexões da IA
        if message.thoughts:
            last_thought = message.thoughts[-1]["thought"]
            print(f"  🤔 Último pensamento: {last_thought[:100]}...")
    
    # === TESTE DIRETO DO ENGINE FÍSICO ===
    print("\n" + "=" * 60)
    print("⚙️ TESTE DIRETO DO ENGINE DE COGNIÇÃO FÍSICA")
    print("-" * 40)
    
    engine = PhysicalCognitionEngine(max_power_watts=100.0)
    
    test_analysis = await engine.analyze_transmission_challenge(
        destination="teste_destino",
        message_size_bytes=1024,  # 1KB
        available_media=[
            TransmissionMedium.WIFI,
            TransmissionMedium.CELLULAR,
            TransmissionMedium.BLUETOOTH,
            TransmissionMedium.COPPER_WIRE
        ],
        estimated_distance=2000.0  # 2km
    )
    
    print("🔬 Análise detalhada:")
    for medium_analysis in test_analysis["medium_analysis"]:
        medium = medium_analysis["medium"]
        feasible = medium_analysis["feasible"]
        energy = medium_analysis["total_energy_required_joules"]
        quality = medium_analysis["quality_score"]
        
        status = "✅ Viável" if feasible else "❌ Inviável"
        print(f"  📡 {medium}: {status} - Energia: {energy:.3f}J - Qualidade: {quality:.2f}")
    
    print(f"\n🎯 Estratégia recomendada: {test_analysis['recommended_strategy']['strategy']}")
    
    print("\n🧠 Reflexões do engine:")
    for reflection in test_analysis["ai_reflections"]:
        print(f"  💭 {reflection}")
    
    print("\n" + "=" * 60)
    print("✅ TESTE COMPLETO FINALIZADO")
    print("=" * 60)

async def demo_android_integration():
    """Demonstra como integrar com o app Android"""
    
    print("\n📱 SIMULAÇÃO DE INTEGRAÇÃO COM APP ANDROID")
    print("-" * 50)
    
    # Simula dados vindos do app Android
    android_data = {
        "available_networks": ["wifi", "cellular", "bluetooth"],
        "signal_strengths": {"wifi": -45, "cellular": -70, "bluetooth": -55},
        "battery_level": 75,  # 75%
        "message_content": "Mensagem do app Android com sniffer de rede",
        "target_bandwidth_mb": 30,
        "current_location": "device_android"
    }
    
    print(f"📊 Dados do Android:")
    for key, value in android_data.items():
        print(f"  {key}: {value}")
    
    # Calcula energia disponível baseada na bateria
    max_power_from_battery = (android_data["battery_level"] / 100.0) * 50.0  # 50W max
    
    # Cria mensagem
    android_message = ThinkingMessage(
        id="android_msg_001",
        content=android_data["message_content"],
        destination="servidor_web",
        source=android_data["current_location"],
        timestamp=time.time(),
        available_power_watts=max_power_from_battery,
        intelligence_level=7
    )
    
    print(f"\n⚡ Energia disponível (baseada na bateria): {max_power_from_battery:.1f}W")
    
    # Executa análise e propagação
    await android_message.autonomous_propagation(android_data["available_networks"])
    
    # Resultado para enviar de volta ao Android
    result = {
        "analysis_complete": True,
        "strategy": android_message.physical_analysis["recommended_strategy"]["strategy"],
        "energy_needed_joules": android_message.physical_analysis["recommended_strategy"].get("energy_required_joules", 0),
        "estimated_time_seconds": android_message.physical_analysis["recommended_strategy"].get("transmission_time_seconds", 0),
        "success_probability": 0.85 if android_message.physical_analysis["recommended_strategy"]["strategy"] != "impossible" else 0.0,
        "ai_reflections": android_message.physical_analysis["ai_reflections"]
    }
    
    print(f"\n📤 Resultado para o Android:")
    for key, value in result.items():
        if key == "ai_reflections":
            print(f"  {key}: {len(value)} reflexões")
        else:
            print(f"  {key}: {value}")

if __name__ == "__main__":
    print("🚀 Iniciando teste completo do sistema...")
    asyncio.run(test_complete_system())
    asyncio.run(demo_android_integration())

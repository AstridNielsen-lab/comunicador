import asyncio
import aiohttp
import json
import time
import uuid
import subprocess
import platform
import socket
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
try:
    import psutil
except ImportError:
    psutil = None

try:
    import netifaces
except ImportError:
    netifaces = None

try:
    import bluetooth
except ImportError:
    bluetooth = None


class NetworkScanner:
    """Scanner real de redes locais"""
    
    def __init__(self, logger):
        self.logger = logger
        self.detected_networks = []
    
    async def scan_local_networks(self) -> List[Dict]:
        """Busca redes locais reais"""
        networks = []
        
        self.logger.log("INFO", "🔍 Iniciando varredura de redes locais...")
        
        # WiFi Networks
        try:
            wifi_networks = await self._scan_wifi()
            networks.extend(wifi_networks)
        except Exception as e:
            self.logger.log("WARNING", f"Erro ao buscar WiFi: {e}")
        
        # Bluetooth Devices
        try:
            bt_devices = await self._scan_bluetooth()
            networks.extend(bt_devices)
        except Exception as e:
            self.logger.log("WARNING", f"Erro ao buscar Bluetooth: {e}")
        
        # Network Interfaces
        try:
            interfaces = await self._scan_interfaces()
            networks.extend(interfaces)
        except Exception as e:
            self.logger.log("WARNING", f"Erro ao buscar interfaces: {e}")
        
        # Network Neighbors
        try:
            neighbors = await self._scan_network_neighbors()
            networks.extend(neighbors)
        except Exception as e:
            self.logger.log("WARNING", f"Erro ao buscar vizinhos: {e}")
        
        self.detected_networks = networks
        self.logger.log("SUCCESS", f"✅ Encontradas {len(networks)} redes/dispositivos")
        
        return networks
    
    async def _scan_wifi(self) -> List[Dict]:
        """Busca redes WiFi disponíveis"""
        networks = []
        
        try:
            if platform.system() == "Windows":
                # Windows netsh command
                result = subprocess.run(
                    ["netsh", "wlan", "show", "profiles"], 
                    capture_output=True, text=True, timeout=10
                )
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if "Perfil de Todos os Usuários" in line or "All User Profile" in line:
                            ssid = line.split(':')[-1].strip()
                            if ssid:
                                networks.append({
                                    "type": "wifi",
                                    "ssid": ssid,
                                    "signal_strength": "unknown",
                                    "security": "unknown",
                                    "detected_at": datetime.now().isoformat()
                                })
                                self.logger.log("NETWORK", f"📶 WiFi encontrado: {ssid}")
            
            elif platform.system() == "Linux":
                # Linux iwlist scan
                result = subprocess.run(
                    ["iwlist", "scan"], 
                    capture_output=True, text=True, timeout=10
                )
                # Parse iwlist output...
                
        except Exception as e:
            self.logger.log("ERROR", f"Erro WiFi scan: {e}")
        
        return networks
    
    async def _scan_bluetooth(self) -> List[Dict]:
        """Busca dispositivos Bluetooth"""
        devices = []
        
        try:
            # Tenta descobrir dispositivos Bluetooth próximos
            if bluetooth and platform.system() == "Windows":
                # Windows bluetooth discovery
                nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True)
                
                for addr, name in nearby_devices:
                    devices.append({
                        "type": "bluetooth",
                        "address": addr,
                        "name": name or "Unknown",
                        "detected_at": datetime.now().isoformat()
                    })
                    self.logger.log("NETWORK", f"📱 Bluetooth: {name} ({addr})")
                    
        except Exception as e:
            self.logger.log("WARNING", f"Bluetooth não disponível: {e}")
        
        return devices
    
    async def _scan_interfaces(self) -> List[Dict]:
        """Lista interfaces de rede ativas"""
        interfaces = []
        
        try:
            if not netifaces:
                self.logger.log("WARNING", "netifaces não disponível")
                return interfaces
                
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        if ip and ip != '127.0.0.1':
                            interfaces.append({
                                "type": "interface",
                                "name": interface,
                                "ip": ip,
                                "netmask": addr_info.get('netmask'),
                                "detected_at": datetime.now().isoformat()
                            })
                            self.logger.log("NETWORK", f"🔌 Interface: {interface} ({ip})")
        
        except Exception as e:
            self.logger.log("ERROR", f"Erro ao listar interfaces: {e}")
        
        return interfaces
    
    async def _scan_network_neighbors(self) -> List[Dict]:
        """Busca dispositivos na rede local"""
        neighbors = []
        
        try:
            # Pega o IP local
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Extrai rede (ex: 192.168.1.x)
            network_base = '.'.join(local_ip.split('.')[:-1])
            
            self.logger.log("INFO", f"🔍 Vasculhando rede {network_base}.x...")
            
            # Ping sweep simplificado (apenas alguns IPs para demonstração)
            for i in [1, 2, 3, 4, 5, 254]:  # IPs comuns
                target_ip = f"{network_base}.{i}"
                
                try:
                    # Ping rápido
                    if platform.system() == "Windows":
                        result = subprocess.run(
                            ["ping", "-n", "1", "-w", "1000", target_ip],
                            capture_output=True, timeout=2
                        )
                    else:
                        result = subprocess.run(
                            ["ping", "-c", "1", "-W", "1", target_ip],
                            capture_output=True, timeout=2
                        )
                    
                    if result.returncode == 0:
                        neighbors.append({
                            "type": "neighbor",
                            "ip": target_ip,
                            "reachable": True,
                            "detected_at": datetime.now().isoformat()
                        })
                        self.logger.log("NETWORK", f"🏠 Vizinho ativo: {target_ip}")
                
                except subprocess.TimeoutExpired:
                    pass
                except Exception:
                    pass
        
        except Exception as e:
            self.logger.log("ERROR", f"Erro ao buscar vizinhos: {e}")
        
        return neighbors


class PublicAPIScanner:
    """Scanner de APIs públicas para coletar informações"""
    
    def __init__(self, logger):
        self.logger = logger
        self.session = None
    
    async def scan_public_apis(self) -> List[Dict]:
        """Busca informações via APIs públicas"""
        api_data = []
        
        self.logger.log("INFO", "🌐 Vasculhando APIs públicas...")
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            self.session = session
            
            # IP público e localização
            try:
                location_data = await self._get_location_info()
                api_data.append(location_data)
            except Exception as e:
                self.logger.log("WARNING", f"Erro API localização: {e}")
            
            # Informações de ISP
            try:
                isp_data = await self._get_isp_info()
                api_data.append(isp_data)
            except Exception as e:
                self.logger.log("WARNING", f"Erro API ISP: {e}")
            
            # Status de serviços públicos
            try:
                services_data = await self._check_public_services()
                api_data.extend(services_data)
            except Exception as e:
                self.logger.log("WARNING", f"Erro API serviços: {e}")
            
            # Dados climáticos (como exemplo)
            try:
                weather_data = await self._get_weather_info()
                api_data.append(weather_data)
            except Exception as e:
                self.logger.log("WARNING", f"Erro API clima: {e}")
        
        self.logger.log("SUCCESS", f"✅ Coletados {len(api_data)} dados de APIs")
        return api_data
    
    async def _get_location_info(self) -> Dict:
        """Pega informações de localização via IP"""
        async with self.session.get("http://ip-api.com/json/") as response:
            data = await response.json()
            
            location_info = {
                "api": "ip-location",
                "ip": data.get("query"),
                "country": data.get("country"),
                "city": data.get("city"),
                "region": data.get("regionName"),
                "isp": data.get("isp"),
                "org": data.get("org"),
                "timezone": data.get("timezone"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
                "detected_at": datetime.now().isoformat()
            }
            
            self.logger.log("NETWORK", f"🌍 Localização: {data.get('city')}, {data.get('country')}")
            self.logger.log("NETWORK", f"📡 ISP: {data.get('isp')}")
            
            return location_info
    
    async def _get_isp_info(self) -> Dict:
        """Informações detalhadas do ISP"""
        async with self.session.get("https://httpbin.org/ip") as response:
            data = await response.json()
            
            isp_info = {
                "api": "isp-info",
                "origin_ip": data.get("origin"),
                "detected_at": datetime.now().isoformat()
            }
            
            return isp_info
    
    async def _check_public_services(self) -> List[Dict]:
        """Verifica status de serviços públicos"""
        services = []
        
        # Lista de serviços para testar
        test_services = [
            {"name": "Google DNS", "url": "https://8.8.8.8"},
            {"name": "Cloudflare DNS", "url": "https://1.1.1.1"},
            {"name": "GitHub", "url": "https://api.github.com"},
        ]
        
        for service in test_services:
            try:
                start_time = time.time()
                async with self.session.get(service["url"]) as response:
                    response_time = (time.time() - start_time) * 1000
                    
                    services.append({
                        "api": "service-check",
                        "service": service["name"],
                        "url": service["url"],
                        "status": response.status,
                        "response_time_ms": round(response_time, 2),
                        "reachable": response.status == 200,
                        "detected_at": datetime.now().isoformat()
                    })
                    
                    status = "✅" if response.status == 200 else "❌"
                    self.logger.log("NETWORK", f"{status} {service['name']}: {round(response_time, 2)}ms")
                    
            except Exception as e:
                services.append({
                    "api": "service-check",
                    "service": service["name"],
                    "url": service["url"],
                    "status": "timeout",
                    "error": str(e),
                    "reachable": False,
                    "detected_at": datetime.now().isoformat()
                })
                self.logger.log("ERROR", f"❌ {service['name']}: {e}")
        
        return services
    
    async def _get_weather_info(self) -> Dict:
        """Exemplo de API adicional - clima"""
        # API gratuita que não precisa de key
        async with self.session.get("https://wttr.in/?format=j1") as response:
            data = await response.json()
            
            current = data.get("current_condition", [{}])[0]
            
            weather_info = {
                "api": "weather",
                "temperature": current.get("temp_C"),
                "humidity": current.get("humidity"),
                "description": current.get("weatherDesc", [{}])[0].get("value"),
                "detected_at": datetime.now().isoformat()
            }
            
            self.logger.log("INFO", f"🌤️ Clima: {current.get('temp_C')}°C, {weather_info['description']}")
            
            return weather_info


class LivingAIPersona:
    """IA persona que vive na mensagem e toma decisões reais"""
    
    def __init__(self, message_id: str, content: str, destination: str, logger):
        self.message_id = message_id
        self.content = content
        self.destination = destination
        self.logger = logger
        
        # Componentes da IA
        self.network_scanner = NetworkScanner(logger)
        self.api_scanner = PublicAPIScanner(logger)
        
        # Estado da IA
        self.current_location = "origin"
        self.anchored_connections = []
        self.discovered_data = []
        self.decision_history = []
        self.exploration_count = 0
    
    async def live_and_explore(self) -> Dict[str, Any]:
        """IA vive e explora o ambiente real"""
        
        self.logger.log("INFO", f"🧠 IA Persona ativada para mensagem {self.message_id[:8]}")
        self.logger.log("INFO", f"🎯 Missão: Entregar '{self.content}' para {self.destination}")
        
        exploration_report = {
            "message_id": self.message_id,
            "start_time": datetime.now().isoformat(),
            "discoveries": [],
            "decisions": [],
            "anchored_points": [],
            "final_status": "exploring"
        }
        
        # Ciclo de vida da IA
        for cycle in range(5):  # 5 ciclos de exploração
            self.exploration_count += 1
            
            self.logger.log("INFO", f"🔄 Ciclo de exploração {cycle + 1}/5")
            
            # 1. Busca redes locais
            local_networks = await self.network_scanner.scan_local_networks()
            
            # 2. Se não houver redes ou poucas redes, busca APIs públicas
            if len(local_networks) < 3:
                self.logger.log("WARNING", "⚠️ Poucas redes locais, buscando APIs públicas...")
                api_data = await self.api_scanner.scan_public_apis()
                local_networks.extend(api_data)
            
            # 3. IA analisa e toma decisões
            decision = await self._make_intelligent_decision(local_networks)
            
            # 4. Executa ação baseada na decisão
            action_result = await self._execute_decision(decision, local_networks)
            
            # 5. Registra descobertas
            exploration_report["discoveries"].extend(local_networks)
            exploration_report["decisions"].append(decision)
            
            if action_result.get("should_anchor"):
                anchor_point = {
                    "location": self.current_location,
                    "reason": action_result.get("anchor_reason"),
                    "timestamp": datetime.now().isoformat(),
                    "networks_available": len(local_networks)
                }
                self.anchored_connections.append(anchor_point)
                exploration_report["anchored_points"].append(anchor_point)
                
                self.logger.log("ANCHOR", f"🔗 IA ancorou em {self.current_location}")
            
            # 6. Simula movimento/progresso
            if action_result.get("move_to"):
                old_location = self.current_location
                self.current_location = action_result["move_to"]
                self.logger.log("MOVEMENT", f"📍 IA moveu de {old_location} -> {self.current_location}")
            
            # 7. Pausa entre ciclos
            await asyncio.sleep(2)
        
        # Status final
        exploration_report["end_time"] = datetime.now().isoformat()
        exploration_report["final_location"] = self.current_location
        exploration_report["total_discoveries"] = len(exploration_report["discoveries"])
        exploration_report["total_anchors"] = len(exploration_report["anchored_points"])
        exploration_report["final_status"] = "completed"
        
        self.logger.log("SUCCESS", f"🎊 IA completou exploração com {len(exploration_report['discoveries'])} descobertas")
        
        return exploration_report
    
    async def _make_intelligent_decision(self, available_data: List[Dict]) -> Dict[str, Any]:
        """IA toma decisão inteligente baseada nos dados coletados"""
        
        # Simula pensamento da IA real (poderia usar Gemini API aqui)
        wifi_count = len([d for d in available_data if d.get("type") == "wifi"])
        bt_count = len([d for d in available_data if d.get("type") == "bluetooth"])
        api_count = len([d for d in available_data if d.get("api")])
        
        self.logger.log("THINKING", f"🤔 IA analisando: {wifi_count} WiFi, {bt_count} Bluetooth, {api_count} APIs")
        
        # Lógica de decisão da IA
        if wifi_count >= 2:
            strategy = "wifi_propagation"
            confidence = 0.8
            reasoning = "Múltiplas redes WiFi disponíveis, propagação direta"
        elif bt_count >= 1:
            strategy = "bluetooth_mesh"
            confidence = 0.6
            reasoning = "Usando Bluetooth para criar rede mesh"
        elif api_count >= 2:
            strategy = "internet_relay"
            confidence = 0.7
            reasoning = "Usando Internet como relay via APIs públicas"
        else:
            strategy = "anchor_and_wait"
            confidence = 0.4
            reasoning = "Poucos recursos, ancorando e aguardando"
        
        decision = {
            "strategy": strategy,
            "confidence": confidence,
            "reasoning": reasoning,
            "data_analyzed": len(available_data),
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.log("THINKING", f"💭 IA decidiu: {strategy} (confiança: {confidence:.1%})")
        self.logger.log("THINKING", f"💡 Raciocínio: {reasoning}")
        
        self.decision_history.append(decision)
        return decision
    
    async def _execute_decision(self, decision: Dict, available_data: List[Dict]) -> Dict[str, Any]:
        """Executa a decisão tomada pela IA"""
        
        strategy = decision["strategy"]
        result = {"executed": True, "strategy": strategy}
        
        if strategy == "wifi_propagation":
            # Simula propagação via WiFi
            wifi_networks = [d for d in available_data if d.get("type") == "wifi"]
            if wifi_networks:
                chosen_network = wifi_networks[0]
                result.update({
                    "move_to": f"wifi_{chosen_network.get('ssid', 'unknown')}",
                    "method": "wifi_connection",
                    "target": chosen_network
                })
                self.logger.log("SUCCESS", f"📶 Conectando via WiFi: {chosen_network.get('ssid')}")
        
        elif strategy == "bluetooth_mesh":
            # Simula criação de mesh Bluetooth
            bt_devices = [d for d in available_data if d.get("type") == "bluetooth"]
            if bt_devices:
                chosen_device = bt_devices[0]
                result.update({
                    "move_to": f"bt_{chosen_device.get('name', 'unknown')}",
                    "method": "bluetooth_mesh",
                    "target": chosen_device
                })
                self.logger.log("SUCCESS", f"📱 Criando mesh com: {chosen_device.get('name')}")
                
        elif strategy == "internet_relay":
            # Simula uso de Internet como relay
            api_data = [d for d in available_data if d.get("api")]
            if api_data:
                chosen_api = api_data[0]
                result.update({
                    "move_to": f"api_{chosen_api.get('api', 'unknown')}",
                    "method": "internet_relay",
                    "target": chosen_api
                })
                self.logger.log("SUCCESS", f"🌐 Usando relay: {chosen_api.get('api')}")
        
        elif strategy == "anchor_and_wait":
            # IA decide ancorar
            result.update({
                "should_anchor": True,
                "anchor_reason": "Aguardando melhores condições de rede",
                "method": "strategic_anchor"
            })
            self.logger.log("ANCHOR", "🔗 IA decidiu ancorar estrategicamente")
        
        return result


# Sistema de teste da IA viva
async def test_living_ai_system():
    """Testa o sistema de IA viva"""
    
    print("🚀 Iniciando Sistema de IA Viva")
    print("=" * 50)
    
    # Logger
    from advanced_messaging_system import RealTimeLogger
    
    captured_logs = []
    def log_callback(log_entry):
        captured_logs.append(log_entry)
    
    logger = RealTimeLogger(log_callback)
    
    # Cria IA persona viva
    ai_persona = LivingAIPersona(
        message_id=str(uuid.uuid4()),
        content="Esta mensagem está VIVA e explorando o mundo real!",
        destination="servidor_destino",
        logger=logger
    )
    
    # IA vive e explora
    exploration_report = await ai_persona.live_and_explore()
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO DE EXPLORAÇÃO DA IA VIVA")
    print("=" * 50)
    
    print(f"🆔 ID da Mensagem: {exploration_report['message_id'][:8]}")
    print(f"⏰ Duração: {exploration_report['start_time']} -> {exploration_report['end_time']}")
    print(f"🔍 Total de Descobertas: {exploration_report['total_discoveries']}")
    print(f"⚓ Pontos de Ancoragem: {exploration_report['total_anchors']}")
    print(f"🧠 Decisões Tomadas: {len(exploration_report['decisions'])}")
    print(f"📍 Localização Final: {exploration_report['final_location']}")
    print(f"📝 Logs Capturados: {len(captured_logs)}")
    
    print(f"\n✅ Status: {exploration_report['final_status']}")
    
    return exploration_report, captured_logs


if __name__ == "__main__":
    # Instala dependências se necessário
    try:
        import psutil
        import netifaces
        import bluetooth
    except ImportError:
        print("⚠️  Algumas bibliotecas podem não estar instaladas:")
        print("pip install psutil netifaces pybluez")
        print("Continuando com funcionalidades limitadas...\n")
    
    asyncio.run(test_living_ai_system())

#!/usr/bin/env python3
"""
Script de inicialização do Servidor de Mensagens Cognitivas

Este script:
1. Instala as dependências necessárias
2. Inicializa o servidor web
3. Fornece interface para envio de mensagens cognitivas
"""

import subprocess
import sys
import os

def install_dependencies():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        sys.exit(1)

def check_files():
    """Verifica se todos os arquivos necessários existem"""
    required_files = [
        "adaptive_messenger.py",
        "cognitive_messenger_web.py", 
        "templates/index.html",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Arquivos não encontrados: {', '.join(missing_files)}")
        sys.exit(1)
    
    print("✅ Todos os arquivos necessários encontrados!")

def start_server():
    """Inicia o servidor web"""
    print("🚀 Iniciando Servidor de Mensagens Cognitivas...")
    print("🌐 Acesse: http://localhost:5000")
    print("📡 Pressione Ctrl+C para parar o servidor")
    
    try:
        import cognitive_messenger_web
    except ImportError as e:
        print(f"❌ Erro ao importar módulo: {e}")
        print("Instalando dependências...")
        install_dependencies()
        import cognitive_messenger_web

if __name__ == "__main__":
    print("=" * 50)
    print("🧠 SERVIDOR DE MENSAGENS COGNITIVAS")
    print("=" * 50)
    print()
    
    # Verifica arquivos
    check_files()
    
    # Pergunta se deve instalar dependências
    response = input("Instalar/atualizar dependências? (s/N): ").lower()
    if response in ['s', 'sim', 'y', 'yes']:
        install_dependencies()
    
    print()
    print("🎯 CARACTERÍSTICAS DO SISTEMA:")
    print("   • Mensagens cognitivas que aprendem rotas")
    print("   • Clonagem automática para melhor disseminação")
    print("   • Nunca perde mensagens até confirmação de entrega")
    print("   • Interface web em tempo real")
    print("   • Varre todas as redes disponíveis")
    print()
    
    # Inicia servidor
    start_server()

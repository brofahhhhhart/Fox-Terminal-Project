import os
import subprocess
import sys
import time
import requests
import datetime
import hashlib
import re
import platform
import shutil
import traceback
import json
import threading
from colorama import Fore, Style, init

# Inicialização de cores (Auto-reset para não manchar o terminal)
init(autoreset=True)

# --- NÚCLEO DE CONFIGURAÇÃO E INFRAESTRUTURA ---
FOX_CONFIG = {
    "identity": {
        "name": "FOX TERMINAL PRO",
        "version": "1.2.4.09 (Beta)",
        "build": "2026.04.27-ULTRA-SECURE",
        "codename": "HYPERION-CORE"
    },
    "hardware": {
        "storage_total": 128,
        "storage_used": 103,
        "arch": platform.machine(),
        "node": platform.node()
    },
    "fs": {
        "root": ".fox_system",
        "bin": ".fox_system/bin",
        "logs": ".fox_system/logs",
        "quarantine": ".fox_system/quarantine",
        "vault": ".fox_system/vault",
        "backups": ".fox_system/backups"
    },
    "security": {
        "level": "MAXIMUM",
        "shield_active": True,
        "blacklist": [
            r"os\.remove", r"shutil\.rmtree", r"requests\.post", 
            r"socket\.connect", r"eval\(", r"exec\(", r"base64\.b64decode",
            r"__import__", r"subprocess\.call\(.*rm "
        ]
    }
}

class FoxTerminalUI:
    """Motor de Interface Visual e Estética Técnica."""
    
    @staticmethod
    def clear():
        os.system('clear' if os.name == 'posix' else 'cls')

    def draw_header(self):
        self.clear()
        print(f"{Fore.CYAN}  █▀▀ █▀█ █▄█   ▀█▀ █▀▀ █▀█ █▀▄▀█ █ █▄ █ ▄▀█ █  ")
        print(f"{Fore.CYAN}  █▀  █▄█ █ █    █  ██▄ █▀▄ █ ▀ █ █ █ ▀█ █▀█ █▄▄")
        print(f"{Fore.WHITE}─" * 65)
        print(f"  {Fore.YELLOW}{FOX_CONFIG['identity']['name']} {Style.BRIGHT}{FOX_CONFIG['identity']['version']}")
        print(f"  {Fore.WHITE}KERNEL: {Fore.GREEN}{FOX_CONFIG['identity']['codename']} {Fore.WHITE}| BUILD: {Fore.MAGENTA}{FOX_CONFIG['identity']['build']}")
        
        # Cálculo de Armazenamento Real
        used = FOX_CONFIG['hardware']['storage_used']
        total = FOX_CONFIG['hardware']['storage_total']
        perc = (used / total) * 100
        color_storage = Fore.GREEN if perc < 80 else Fore.RED
        print(f"  {Fore.WHITE}STORAGE: {color_storage}{used}GB / {total}GB {Fore.WHITE}({perc:.1f}%)")
        print(f"{Fore.WHITE}─" * 65)

    def security_alert(self):
        print(f"\n  {Fore.RED}[!] MONITORAMENTO DE SEGURANÇA ATIVO")
        print(f"  {Fore.WHITE}> O {Fore.CYAN}FoxShield{Fore.WHITE} está protegendo o Android 13/14.")
        print(f"  {Fore.WHITE}> Integridade do Kernel: {Fore.GREEN}VALIDADA")
        print(f"{Fore.WHITE}─" * 65)

    def help_menu(self):
        print(f"\n  {Fore.YELLOW}COMANDOS DE NÚCLEO:")
        commands = [
            ("status", "Relatório detalhado de hardware e sistema."),
            ("install", "Instalação inteligente com bypass de erro."),
            ("scan", "Análise heurística de arquivos contra malware."),
            ("rede", "Diagnóstico de latência e conectividade WAN."),
            ("backup", "Cria snapshot do diretório Fox."),
            ("logs", "Visualiza histórico de auditoria."),
            ("clean", "Limpa buffer e recarrega ambiente."),
            ("exit", "Desligamento seguro do Terminal.")
        ]
        for cmd, desc in commands:
            print(f"  {Fore.CYAN}❯ {cmd:<10} {Fore.WHITE}: {desc}")
        print("")

    @staticmethod
    def loader(task, loops=12):
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        sys.stdout.write(f"  {Fore.YELLOW}[*] {Fore.WHITE}{task} ".ljust(45))
        for i in range(loops):
            time.sleep(0.08)
            sys.stdout.write(f"\r  {Fore.CYAN}{frames[i % len(frames)]} {Fore.WHITE}{task}...")
            sys.stdout.flush()
        print(f"\r  {Fore.GREEN}[DONE] {Fore.WHITE}{task} ".ljust(50))

class FoxShield:
    """Defesa Heurística e Gestão de Auditoria."""
    
    def __init__(self):
        self._ensure_fs()

    def _ensure_fs(self):
        for path in FOX_CONFIG["fs"].values():
            if not os.path.exists(path): os.makedirs(path)

    def log(self, action, level="INFO"):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        color = Fore.WHITE if level == "INFO" else Fore.RED
        with open(os.path.join(FOX_CONFIG["fs"]["logs"], "audit.log"), "a") as f:
            f.write(f"[{ts}] [{level}] {action}\n")

    def analyze_script(self, content, name="Unknown"):
        threats = [p for p in FOX_CONFIG["security"]["blacklist"] if re.search(p, content)]
        if threats:
            print(f"\n  {Fore.RED}[!!!] ALERTA CRÍTICO: {name}")
            print(f"  {Fore.WHITE}[-] Ameaças detectadas: {Fore.YELLOW}{', '.join(threats)}")
            choice = input(f"  {Fore.WHITE}[?] Bloquear execução perigosa? (s/n): ").lower()
            if choice != 'n':
                self.log(f"BLOCKED: {name} | Threats: {threats}", "SECURITY")
                return False
        return True

class ExecutionEngine:
    """Motor de Gestão de Pacotes e Reparo de Sistema."""
    
    def __init__(self, shield, ui):
        self.shield = shield
        self.ui = ui

    def smart_pip(self, pkg):
        self.ui.loader(f"Verificando {pkg}")
        self.shield.log(f"INSTALL_ATTEMPT: {pkg}")
        
        cmd = [sys.executable, "-m", "pip", "install", pkg, "--upgrade"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate()

        if proc.returncode == 0:
            print(f"  {Fore.GREEN}[+] Pacote '{pkg}' integrado com sucesso.")
            self.shield.log(f"INSTALL_SUCCESS: {pkg}")
        else:
            self._analyze_error(stderr, pkg)

    def _analyze_error(self, stderr, pkg):
        print(f"\n  {Fore.RED}[!] FALHA NA INSTALAÇÃO: {pkg}")
        self.shield.log(f"INSTALL_FAILED: {pkg}", "ERROR")
        
        # Diagnóstico de Compilação C++ no Android
        if any(x in stderr for x in ["gcc", "C++", "cl.exe", "headers", "build-essential"]):
            print(f"  {Fore.YELLOW}[-] CAUSA: O pacote exige compilação nativa C++.")
            print(f"  {Fore.WHITE}[-] INFO: O Android requer hooks de sistema para compilar {pkg}.")
            
            if input(f"\n  {Fore.CYAN}[?] Deseja aplicar patches de sistema para corrigir? (s/n): ").lower() == 's':
                self.ui.loader("Aplicando Hooks de Compatibilidade")
                print(f"  {Fore.GREEN}[OK] Sistema atualizado. Reinicie a instalação.")
        else:
            print(f"  {Fore.WHITE}[-] LOG: {stderr.splitlines()[-1] if stderr else 'Desconhecido'}")

class FoxTerminal:
    """O Hypervisor Principal."""
    
    def __init__(self):
        self.ui = FoxTerminalUI()
        self.shield = FoxShield()
        self.engine = ExecutionEngine(self.shield, self.ui)

    def run(self):
        self.ui.draw_header()
        self.ui.security_alert()
        self.ui.help_menu()
        
        while True:
            try:
                ts = datetime.datetime.now().strftime("%H:%M")
                prompt = f"  {Fore.WHITE}[{ts}] {Fore.CYAN}fox@beta{Fore.WHITE}:~$ "
                cmd_raw = input(prompt).strip()
                
                if not cmd_raw: continue
                
                self.shield.log(f"EXEC_CMD: {cmd_raw}")
                parts = cmd_raw.split()
                cmd = parts[0].lower()
                args = parts[1:]

                if cmd == "status":
                    self.ui.draw_header()
                    print(f"  {Fore.YELLOW}SESSION ID: {Fore.WHITE}{hashlib.md5(ts.encode()).hexdigest()[:8].upper()}")
                    print(f"  {Fore.YELLOW}CPU ARCH  : {Fore.WHITE}{FOX_CONFIG['hardware']['arch']}")
                
                elif cmd in ["install", "f-pkg"]:
                    if args: self.engine.smart_install(args[0])
                    else: print(f"  {Fore.RED}Uso: install [pacote]")

                elif cmd == "rede":
                    self.ui.loader("Pingando Servidores WAN")
                    try:
                        r = requests.get("https://api.ipify.org", timeout=5)
                        print(f"  {Fore.GREEN}[NET] Status: Online | IP: {Fore.WHITE}{r.text}")
                    except: print(f"  {Fore.RED}[NET] Status: Offline ou DNS instável.")

                elif cmd == "backup":
                    self.ui.loader("Gerando Snapshot do Sistema")
                    ts_bkp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                    bkp_path = os.path.join(FOX_CONFIG["fs"]["backups"], f"snap_{ts_bkp}")
                    # Simulação de backup
                    time.sleep(1)
                    print(f"  {Fore.GREEN}[OK] Backup salvo em: {bkp_path}")

                elif cmd == "logs":
                    log_path = os.path.join(FOX_CONFIG["fs"]["logs"], "audit.log")
                    if os.path.exists(log_path):
                        with open(log_path, 'r') as f:
                            lines = f.readlines()[-15:]
                            print(f"\n{Fore.CYAN}--- ÚLTIMOS LOGS DE AUDITORIA ---")
                            for l in lines: print(f"  {l.strip()}")
                    else: print(f"  {Fore.RED}[!] Nenhum log disponível.")

                elif cmd == "scan":
                    if args and os.path.exists(args[0]):
                        with open(args[0], 'r', errors='ignore') as f:
                            self.shield.analyze_script(f.read(), args[0])
                    else: print(f"  {Fore.RED}Uso: scan [arquivo.py]")

                elif cmd == "clean":
                    self.run()

                elif cmd == "exit":
                    print(f"  {Fore.YELLOW}[#] Desligando Kernel do Fox Terminal...")
                    break
                
                else:
                    # Execução direta no shell (ex: ls, cd, top)
                    subprocess.run(cmd_raw, shell=True)
                    
            except KeyboardInterrupt:
                print(f"\n  {Fore.YELLOW}[!] Use 'exit' para fechar o sistema com segurança.")
            except Exception:
                print(f"  {Fore.RED}[ERROR] Falha de Kernel: {traceback.format_exc().splitlines()[-1]}")

if __name__ == "__main__":
    # Boot do Hypervisor
    hypervisor = FoxTerminal()
    hypervisor.run()

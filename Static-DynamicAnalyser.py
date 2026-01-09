import os
import time
import json
import math
import docker
import yara
from collections import Counter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import hashlib
import re
from malwarebazaar import Bazaar

class UnifiedMalScope:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.yara_rules = self._compile_yara()
        self.n8n_url = "http://localhost:5678/webhook-test/61dab5ad-7b4a-457e-be1e-0e5837140a3a"
        self.bazaar_url = "https://mb-api.abuse.ch/api/v1/"
        self.bazaar = Bazaar("043fc0a2ef95878a237330bc82e73dbadb0e133bd8ade21")
        self.indicators = {
            "Network": [r"http://", r"https://", r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"],
            "Commands": [r"rm ", r"chmod", r"sudo", r"nc -e", r"exec"],
            "Files": [r"/etc/passwd", r"/etc/shadow", r".bashrc"]
        }
    def _compile_yara(self):
        source = """
        rule suspicious_behavior {
            strings:
                $s1 = "eval(base64_decode"
                $s2 = "os.system("
                $s3 = "subprocess.Popen"
            condition:
                any of them
        }   """
        return yara.compile(source=source)

## analisis de metadata ##

    def get_file_metadata(self, file_path, data):
        sha256 = hashlib.sha256(data).hexdigest()
        strings = re.findall(b"[\\x20-\\x7E]{4,}", data)
        decoded_strings = [s.decode('utf-8', errors='ignore') for s in strings]
        matches = []
        for category, patterns in self.indicators.items():
            for pattern in patterns:
                for s in decoded_strings:
                    if re.search(pattern, s):
                        matches.append({"type": category, "pattern": pattern, "context": s[:50]})
        return sha256, matches
    
## calculo de entropia ##

    def calculate_entropy(self, data):
        if not data:
            return 0.0
        occurences = Counter(data)
        file_size = len(data)
        return -sum ((count / file_size) * math.log2(count / file_size) for count in occurences.values())

## Chequear el hash en MalwareBazaar ##

    def check_malware_bazaar(self, sha256):
        try:
            result = self.bazaar.query_hash(sha256)
            if result.get('query_status') == 'ok':
                    data = result['data'][0]
                    return {
                        'known': True,
                        'status': "detected",
                        'signature': data.get('signature'),
                        'tags': data.get('tags'),
                        'file_type': data.get('file_type')
                 }
            return {'known': False, 'status': "not_found", 'message': 'Hash not found in MalwareBazaar.'}
        except Exception as e:
               return {
                     'known': False,
                     'status': "error",
                     'message': f"Error en malware bazaar: {str(e)}"
               }
        
## Ejecución en sandbox Docker ##

    def run_sandbox(self, file_path):
        file_name = os.path.basename(file_path)
        folder = os.path.dirname(file_path)
        try:
            container = self.docker_client.containers.run(
                image = "python:3.9-slim",
                command = f"python /mnt/{file_name}",
                volumes = {folder: {'bind': '/mnt', 'mode': 'ro'}},
                network_disabled = True,
                mem_limit = '128m',
                remove = True,
                detach = False,
                stdout = True,
                stderr = True
            )
            return container.decode('utf-8')
        except Exception as e:
            return f"Sandbox Error: {str(e)}"

## enviar a n8n ##
    def analyze_and_send(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        sha256, matches = self.get_file_metadata(file_path, data)
        malware_data = self.check_malware_bazaar(sha256)
        entropy = self.calculate_entropy(data)
        yara_matches = [m.rule for m in self.yara_rules.match(file_path)]
        sandbox_logs = self.run_sandbox(file_path)
        report = {
            "filename": os.path.basename(file_path),
            "sha256": sha256,
            "malware_bazaar": malware_data,
            "entropy": round(entropy, 4),
            "yara_matches": yara_matches,
            "sandbox_output": sandbox_logs[:500],
            "threat_level": "HIGH" if entropy > 7.0 or yara_matches or matches else "LOW",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            requests.post(self.n8n_url, json=report, timeout=5)
            print(f"[*] Reporte de {report['filename']} enviado a n8n.")
        except Exception as e:
            print(f"[!] Error al enviar reporte a n8n: {str(e)}")

class SandboxHandler(FileSystemEventHandler):
    def __init__(self):
        self.engine = UnifiedMalScope()
    def on_created(self, event):
        if not event.is_directory:
            print(f"[*] Nuevo archivo detectado: {event.src_path}")
            time.sleep(1)
            self.engine.analyze_and_send(event.src_path)

if __name__ == "__main__":
    path = os.path.expanduser("~/Downloads/sandbox")
    if not os.path.exists(path):
        os.makedirs(path)
    observer = Observer()
    observer.schedule(SandboxHandler(), path, recursive=False)
    print(f"[*] Monitoreando la carpeta: {path}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
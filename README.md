# N8N-Automation
Estos son proyectos de automatización de procesos de ciberseguridad en N8N para aprender, practicar y probar conceptos y estrategias
<br><br>
**🐧Linux Threat Hunter**
  <br>
Este proyecto es un sistema IDR SIEM automatizado, privado y procesado por IA local. 
<br>
Implementa una solución automatizada para la protección de sistemas Arch Linux frente a ataques brute-force sobre el servicio SSH <br>
Este workflow orquestado por N8N vigila de forma periódica los registros de sistema de Linux (journalctl), extrae datos clave de ellos y utiliza un agente de IA Llama3 (hosteado localmente) para analizar cada evento en busca de amenazas y anomalías, asignando un valor numérico de riesgo en escala 1-10 y permitiendo realizar acciones si la severidad de la amenaza es ≥ 7 . Todo este proceso es almacenado en bases de datos vía integración con PostgreSQL en la medida en que un evento es detectado y luego procesado por la IA.
<br>
Características
<br>
💻Ingesta automatizada de datos.<br>
🤖Integración con IA local para el análisis de registros.<br>
🛡️100% self-hosted para entornos que requieren privacidad.<br>
🏰Defensa en profundidad con controles preventivos(firewall), detectivos(análisis de registros) y de monitoreo(alertas via email). <br>
💂‍♂️Reducción del MTTR mediante el bloqueo automático de IPs maliciosas.
🐍Parsing inteligente con Python para limpieza e identificación de datos clave.<br>
🐘Almacenamiento pre y post procesamiento en PostgreSQL para realizar auditorías.

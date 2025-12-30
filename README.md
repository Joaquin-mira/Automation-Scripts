# N8N-Automation
Estos proyectos son simples pruebas de concepto de automatización de procesos de ciberseguridad en N8N para aprender, practicar y experimentar con la capacidad de expansión e integración de los workflows orquestados por N8N.
<br><br>
**🐧Linux Threat Hunter**
  <br>
Este proyecto es un sistema SIEM automatizado, privado y procesado por IA local. 
<br>
Implementa una solución automatizada para la protección de sistemas Arch Linux  <br>
Este workflow orquestado por N8N vigila de forma periódica los registros de sistema de Linux (journalctl), extrae datos clave de ellos mediante parsing y utiliza un agente de IA Llama3 (hosteado localmente) para analizar heurísticamente cada evento en busca de amenazas y anomalías, asignando un valor numérico de riesgo en escala 1-10 y permitiendo priorizar la respuesta si la severidad de la amenaza es ≥ 7. <br>
Todo los registros son guardados en bases de datos mediante integración con PostgreSQL al momento de su captura y parseo para facilitar el seguimiento, actualizándose automáticamente la base de datos en la medida en que cada registro es procesado por la IA.
<br>
Características
<br>
💻Ingesta automatizada de datos.<br>
🤖Integración con IA autohospedada para identificar anomalías que el análisis por firmas convencional no detecta mediante análisis de registros.<br>
🛡️100% self-hosted para entornos que requieren privacidad.<br>
🐍Parsing inteligente con Python para limpieza e identificación de datos clave.<br>
🐘Almacenamiento pre y post procesamiento en PostgreSQL para realizar auditorías y mantener integridad.
<br> <br>

**🍯Honeypot integrado con análisis de LLM** <br>
Este proyecto es infraestructura SOAR para capturar intentos de intrusión mediante una trampa informática aislada en Docker basada en Flask y análisis con IA autohospedada. <br>
Se despliega un señuelo que simula ser un log-in administrativo para atraer a atacantes que hayan infiltrado el sistema. Datos clave del atacante como su IP y sus inputs en la trampa son capturados y enviados a N8N mediante webhook para orquestar su procesamiento con Llama3, que recoge el input y lo analiza. La IA genera un output en formato JSON con el tipo de ataque detectado, el nivel de riesgo que representa al sistema y una sugerencia de solución. <br>
La información del atacante y el análisis de la IA son guardados en bases de datos mediante integración con PostreSQL para poder auditar el trabajo de la IA y los ataques detectados. <br>
Además, se automatiza la notificación via Email al equipo SOC con los datos del atacante para brindar mayor información y dar alerta y se bloquea automáticamente la IP del atacante.
<br>
Características
<br>
🛡️100% self-hosted para entornos que requieren privacidad.<br>
🐍Parsing con Python para limpieza e identificación de datos clave.<br>
🐘Almacenamiento vía PostgreSQL para realizar auditorías y mantener integridad.
🏰 Registros persistentes de cada intrusión, alertas via Gmail API para alertar al equipo SOC y bloqueo automático de IPs para reducción de MTTR y defensa en tiempo real

# %%
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from dataLoading import DB_URL
# %%
def generar_datos_facturacion(n_registros = 5000):
    proveedores = [f"PROV-{i:03d}" for i in range(1, 51)]
    empleados = [f"EMP-{i:03d}" for i in range(1, 51)]
    fecha_inicio = datetime(2025, 1, 1)

    data = {
        'transaccion_id': range(0, 0 + n_registros),
        'fecha': [(fecha_inicio + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d") for _ in range(n_registros)],
        'empleado_id': [random.choice(empleados) for _ in range(n_registros)],
        'proveedor_id': [random.choice(proveedores) for _ in range(n_registros)],
        'monto': [round(random.uniform(50.0, 4500.0), 2) for _ in range(n_registros)],
        'categoria': [random.choice(['IT', 'Insumos', 'Logística', 'Marketing']) for _ in range(n_registros)],
    } 
    df = pd.DataFrame(data)
    df['tipo'] = 'legitimo'

    casos_fraude = []
    emp_complice = random.choice(empleados)
    prov_complice = random.choice(proveedores)
    print(f"[+] Empleado cómplice: {emp_complice}, Proveedor cómplice: {prov_complice}")

    for i in range(6):
        fechas_fraude = random.randint(0, 365)
        fecha_fraude = (fecha_inicio + timedelta(days = fechas_fraude)).strftime("%Y-%m-%d")
        monto_total = random.randint(5500, 7000) + 0.99

        partes = []
        restante = monto_total
        for j in range(4):
            p = round(random.uniform(1000.0, 1300.0), 2)
            partes.append(p)
            restante -= p
        partes.append(round(restante, 2))

        for j, monto_fragmento in enumerate(partes):
            casos_fraude.append({
                'transaccion_id': 9000 + (i*5) + j,
                'fecha': fecha_fraude,
                'empleado_id': emp_complice,
                'proveedor_id': prov_complice,
                'monto': monto_fragmento,
                'categoria': random.choice(['IT', 'Insumos', 'Logística', 'Marketing']),
                'tipo': 'fraude'
            })

    df_final = pd.concat([df, pd.DataFrame(casos_fraude)], ignore_index=True)
    df_final.to_csv('transacciones_auditoria.csv', index=False)
    print(F"[+] Dataset generado con {len(df_final)} registros en 'transacciones_auditoria.csv'")  


def visualizar_datos_facturacion(df):
    df['fecha_dt'] = pd.to_datetime(df['fecha'])
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.histplot(
        data=df, x='monto', hue='tipo',
        kde=True, element="step",
        palette={'legitimo': '#3498db', 'fraude': '#e74c3c'}
        )
    plt.title('Distribución de Montos legítimos y posible fraude')
    plt.show() 
# %%
def cargar_datos_facturacion():
    try:
        engine = create_engine(DB_URL)
        print("[*] Leyendo el archivo CSV")
        df = pd.read_csv('transacciones_auditoria.csv')

        print("[*] Cargando datos en la base de datos")
        df.to_sql('facturas_auditoria', engine, if_exists='replace', index=False)
        print("[+] Datos cargados exitosamente en la tabla 'facturas_auditoria'")
    except Exception as e:
        print(f"[!] Error al cargar datos en la base de datos: {e}")


if __name__ == "__main__":
    generar_datos_facturacion()
    visualizar_datos_facturacion(pd.read_csv('transacciones_auditoria.csv'))
    cargar_datos_facturacion()


# %%

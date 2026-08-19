# main.py
# Script de entrada para el Simulador Age of Conquest

from models import Territorio, Faccion
from engine import MotorSimulacion

def main():
    print("==================================================")
    print("   MOTOR LÓGICO DE SIMULACIÓN: AGE OF CONQUEST    ")
    print("==================================================")
    
    # 1. Configuración de Estado Inicial (t = 0)
    # Faccion: Nombre, Tesoro Inicial, Costo de Mantenimiento por unidad
    imperio = Faccion(nombre="Imperio de Jade", tesoro_inicial=200.0, costo_mantenimiento_unitario=15.0)
    rebeldes = Faccion(nombre="Rebeldes del Sur", tesoro_inicial=50.0, costo_mantenimiento_unitario=10.0)
    
    # Configuración de tropas: 40 unidades a 15 de costo = 600 de gasto militar por turno.
    imperio.ejercito = 40 
    rebeldes.ejercito = 25
    
    # Territorios: Nombre, Poblacion, Capacidad Carga (K), Tasa Impositiva (I)
    capital = Territorio(nombre="Capital Primus", poblacion_inicial=1000, capacidad_carga=5000, tasa_impositiva=0.4)
    provincia = Territorio(nombre="Frontera Norte", poblacion_inicial=300, capacidad_carga=800, tasa_impositiva=0.2)
    
    imperio.agregar_territorio(capital)
    imperio.agregar_territorio(provincia)
    
    print("\n--- Estado Inicial (t=0) ---")
    print(f"Facción: {imperio.nombre}")
    print(f"Tesoro: {imperio.tesoro} oro | Ejército Activo: {imperio.ejercito} tropas")
    print(f"Gasto Militar Proyectado: {imperio.calcular_gasto_militar()} oro")
    print("----------------------------")
    
    # 2. Inicialización del Motor Lógico
    motor = MotorSimulacion()
    
    # 3. Carga de la Lista de Eventos Futuros (LEF) para el Turno 1
    # Programamos primero el crecimiento poblacional y luego la economía,
    # garantizando que los impuestos se cobren sobre la población ya actualizada.
    motor.programar_evento(tiempo=1, tipo="POBLACION", referencia=imperio)
    motor.programar_evento(tiempo=1, tipo="ECONOMIA", referencia=imperio)
    
    # Programamos el ataque para el Turno 2
    # Nota que pasamos una tupla (atacante, defensor) como referencia
    motor.programar_evento(tiempo=2, tipo="ATAQUE", referencia=(imperio, rebeldes))
    
    # 4. Bucle de Simulación (Ejecución de al menos 5 fases consecutivas)
    print("\nIniciando secuencia de simulación discreta...")
    
    # Ejecutamos eventos mientras el motor siga activo (reloj <= 5)
    while motor.activo and motor.reloj <= 5:
        motor.ejecutar_turno()
        
    print("\n==================================================")
    print("        SIMULACIÓN FINALIZADA CON ÉXITO           ")
    print("==================================================")

if __name__ == "__main__":
    main()
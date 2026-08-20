# engine.py
import heapq
from models import Faccion, Territorio
from combat import ModeloCombate

class MotorSimulacion:
    def __init__(self):
        self.reloj = 0
        self.lef = []  
        self.facciones = []
        self.activo = True
        self.historial_logs = []  # <-- 1. Inicializamos la lista de captura
        self.historial_metricas = []

    def log(self, mensaje: str):
        """2. Método centralizado para capturar texto para la web y la consola."""
        self.historial_logs.append(mensaje)
        print(mensaje) # Lo mantenemos en consola también para que puedas depurar

    def registrar_metrica_turno(self, faccion):
        """Guarda una 'foto' del estado de la facción al final del turno."""
        poblacion_total = sum(t.poblacion for t in faccion.territorios)
        self.historial_metricas.append({
            "turno": self.reloj,
            "faccion": faccion.nombre,
            "tesoro": round(faccion.tesoro, 2),
            "ejercito": faccion.ejercito,
            "poblacion": round(poblacion_total, 2)
        })
    
    def programar_evento(self, tiempo, tipo, referencia):
        heapq.heappush(self.lef, (tiempo, tipo, referencia))

    def ejecutar_turno(self):
        if not self.lef:
            self.activo = False
            return

        tiempo, tipo, referencia = heapq.heappop(self.lef)
        self.reloj = tiempo

        if tipo == "ECONOMIA":
            faccion = referencia
            self.log(f"\n--- Turno {self.reloj} | Ejecutando: ECONOMIA para {faccion.nombre} ---")
            
            # 1. Se calculan los Ingresos: sumatoria de (poblacion * tasa_impositiva) de cada territorio
            ingresos = faccion.calcular_ingresos_totales()

            # 2. Se calculan los Gastos: G(M) = tropas activas * costo unitario
            gastos = faccion.calcular_gasto_militar()

            # 3. Balance Neto de la iteración
            balance = ingresos - gastos
            
            # 4. EVOLUCIÓN DEL TESORO (E_{t+1} = E_t + Balance)
            faccion.tesoro += balance

            self.log(f"Tesoro: {faccion.tesoro:.2f} | Ingresos: {ingresos:.2f} | Gastos: {gastos:.2f}")

            if faccion.tesoro < 0: #D_t < 0
                desercion = int(abs(faccion.tesoro) / faccion.costo_unitario)
                faccion.ejercito = max(0, faccion.ejercito - desercion)
                faccion.tesoro = 0
                self.log(f"¡ALERTA! Bancarrota. Han desertado {desercion} unidades.")

            self.registrar_metrica_turno(faccion)

        elif tipo == "POBLACION":
            faccion = referencia
            self.log(f"\n--- Turno {self.reloj} | Ejecutando: POBLACION para {faccion.nombre} ---")
            for t in faccion.territorios:
                t.actualizar_poblacion(tasa_crecimiento=0.05)
                self.log(f"Territorio {t.nombre}: Población actualizada a {t.poblacion:.2f}")

        elif tipo == "ATAQUE":
            atacante, defensor = referencia
            self.log(f"\n--- Turno {self.reloj} | Ejecutando: ATAQUE de {atacante.nombre} a {defensor.nombre} ---")
            simulador_batalla = ModeloCombate()
            
            # 3. Pasamos nuestro recolector de logs al modelo de combate
            supervivientes_att, supervivientes_def = simulador_batalla.resolver_batalla(
                tropas_atacante=atacante.ejercito, 
                moral_atacante=atacante.moral,        
                tropas_defensor=defensor.ejercito, 
                moral_defensor=defensor.moral,        
                nivel_defensa=1.2, 
                tropas_provincia=10,
                logger_func=self.log
            )
            
            atacante.ejercito = supervivientes_att
            defensor.ejercito = supervivientes_def
            
            self.log(f"Estado Post-Combate -> {atacante.nombre}: {atacante.ejercito} tropas | {defensor.nombre}: {defensor.ejercito} tropas")

        if self.facciones:
            faccion_principal = self.facciones[0] # O tu facción evaluada
        else:
            # Si no guardaste facciones en una lista, buscamos la referencia si es Facción o tupla
            if isinstance(referencia, tuple):
                faccion_principal = referencia[0] # El atacante
            else:
                faccion_principal = referencia
                
        self.registrar_metrica_turno(faccion_principal)
        
        # Programar los eventos cíclicos
        if tipo in ["ECONOMIA", "POBLACION"] and self.reloj < 5:
            self.programar_evento(self.reloj + 1, tipo, referencia)


    def ejecutar_y_capturar_logs(self, fases: int) -> dict:
        """4. Método orquestador llamado desde FastAPI."""
        self.log("Iniciando secuencia de simulación discreta...")
        
        # Ejecutamos eventos mientras el motor siga activo
        while self.activo and self.reloj <= fases:
            self.ejecutar_turno()
            
        self.log("\n==================================================")
        self.log("        SIMULACIÓN FINALIZADA CON ÉXITO           ")
        self.log("==================================================")
        
        # Devolvemos toda la traza guardada a la web
        return {
            "logs": self.historial_logs,
            "metricas": self.historial_metricas
        }
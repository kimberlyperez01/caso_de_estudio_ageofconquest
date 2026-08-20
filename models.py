# models.py
# Arquitectura de Clases Base para el Motor Lógico de Age of Conquest

class Territorio:
    def __init__(self, nombre: str, poblacion_inicial: float, capacidad_carga: float, tasa_impositiva: float, moral_inicial: float = 100.0):
        self.nombre = nombre
        self.poblacion = poblacion_inicial          # P_t: Variable de estado poblacional
        self.capacidad_carga = capacidad_carga      # K_i: Asíntota poblacional
        self.tasa_impositiva = tasa_impositiva      # I_i: Parámetro de impuesto por habitante
        self.moral = moral_inicial                  # mu: Variable de estado de moral [0, 100]

    def actualizar_poblacion(self, tasa_crecimiento: float):
        """Aplica la ecuación logística de crecimiento poblacional con capacidad de carga."""
        # Condición de frontera: P_t < K_i
        if self.poblacion < self.capacidad_carga:

            # Delta P = r * P_t * (1 - P_t / K_i)
            delta_p = tasa_crecimiento * self.poblacion * (1.0 - (self.poblacion / self.capacidad_carga))

            # Evolución de la población P_{t+1} = P_t + Delta P
            self.poblacion += delta_p
            # Asegurar condición de frontera superior
            if self.poblacion > self.capacidad_carga:
                self.poblacion = self.capacidad_carga
        else:
            self.poblacion = self.capacidad_carga

class Faccion:
    def __init__(self, nombre: str, tesoro_inicial: float, costo_mantenimiento_unitario: float, moral=100.0):
        self.nombre = nombre
        self.tesoro = tesoro_inicial                  # E_t: Variable de estado económica
        self.moral = moral
        self.ejercito = 0                             # M_t: Número total de unidades militares activas
        self.costo_unitario = costo_mantenimiento_unitario
        self.territorios: list[Territorio] = []

    def agregar_territorio(self, territorio: Territorio):
        self.territorios.append(territorio)

    def calcular_ingresos_totales(self) -> float:
        """Calcula la sumatoria de impuestos recaudados en todos sus territorios."""
        ingresos = sum(t.tasa_impositiva * t.poblacion for t in self.territorios)
        return ingresos

    def calcular_gasto_militar(self) -> float:
        """G(M): Gasto total de mantenimiento del ejército activo."""
        return self.ejercito * self.costo_unitario

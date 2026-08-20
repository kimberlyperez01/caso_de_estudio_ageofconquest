# combat.py
# Modelo de Resolución de Combate - Lanchester Estocástico (Versión Avanzada)

import random
import math

class ModeloCombate:
    def __init__(self, letalidad_base_A: float = 0.1, letalidad_base_D: float = 0.1, multiplicador_guarnicion: float = 0.05):
        self.A_A = letalidad_base_A
        self.D_D = letalidad_base_D
        self.G = multiplicador_guarnicion

    def resolver_batalla(self, 
                         tropas_atacante: int, moral_atacante: float, 
                         tropas_defensor: int, moral_defensor: float,
                         nivel_defensa: float = 1.2, tropas_provincia: int = 10,
                         logger_func=print) -> tuple[int, int]: # <-- 1. Añadimos logger_func con un valor por defecto
        
        logger_func("\n=== INICIO DE COMBATE AVANZADO ===")
        logger_func(f"Fuerza Atacante: {tropas_atacante} (Moral: {moral_atacante}) | Fuerza Defensora: {tropas_defensor} (Moral: {moral_defensor})")

        ronda = 1
        while tropas_atacante > 0 and tropas_defensor > 0:
            # 1. Generación de variables aleatorias: Distribución Normal N(1.0, 0.02)
            friccion_A = random.gauss(1.0, 0.02)
            friccion_D = random.gauss(1.0, 0.02)

            # 2. Aplicación de las Ecuaciones Avanzadas de Lanchester
            poder_atacante = self.A_A * tropas_atacante * (moral_atacante / 100.0) * friccion_A
            
            fuerza_base_def = (self.D_D + (self.G * tropas_provincia))
            poder_defensor = fuerza_base_def * tropas_defensor * nivel_defensa * (moral_defensor / 100.0) * friccion_D

            # 3. Cálculo de bajas cruzadas
            bajas_defensor = math.ceil(poder_atacante)
            bajas_atacante = math.ceil(poder_defensor)

            # 4. Actualización de estado
            tropas_atacante = max(0, tropas_atacante - bajas_atacante)
            tropas_defensor = max(0, tropas_defensor - bajas_defensor)

            # 5. Usamos logger_func para registrar cada ronda de manera limpia
            logger_func(f"Ronda {ronda} | Bajas Atte: {bajas_atacante} (Quedan {tropas_atacante}) | Bajas Def: {bajas_defensor} (Quedan {tropas_defensor})")
            ronda += 1

        # 6. Resolución final capturada en el log
        if tropas_atacante > 0:
            logger_func(">>> RESULTADO: ¡Victoria del Atacante! <<<")
        elif tropas_defensor > 0:
            logger_func(">>> RESULTADO: ¡Victoria del Defensor! <<<")
        else:
            logger_func(">>> RESULTADO: Aniquilación mutua. <<<")

        logger_func("==================================\n")
        return tropas_atacante, tropas_defensor

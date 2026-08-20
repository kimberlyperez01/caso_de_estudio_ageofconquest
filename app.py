# app.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn

from models import Faccion, Territorio
from engine import MotorSimulacion

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def mostrar_interfaz(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "logs": None})

@app.post("/")
def ejecutar_simulacion_web(
    request: Request, 
    tesoro_inicial: float = Form(200.0), 
    tropas_imperio: int = Form(40),
    tropas_rebeldes: int = Form(25)
):
    # 1. Instanciamos con los datos del formulario web
    imperio = Faccion(nombre="Imperio de Jade", tesoro_inicial=tesoro_inicial, costo_mantenimiento_unitario=15.0)
    imperio.ejercito = tropas_imperio
    
    capital = Territorio("Capital Primus", 1000, 5000, 0.4)
    frontera = Territorio("Frontera Norte", 300, 800, 0.2)
    imperio.agregar_territorio(capital)
    imperio.agregar_territorio(frontera)
    
    rebeldes = Faccion(nombre="Rebeldes del Sur", tesoro_inicial=50.0, costo_mantenimiento_unitario=10.0)
    rebeldes.ejercito = tropas_rebeldes
    
    # 2. Inicializamos el Motor y cargamos la LEF
    motor = MotorSimulacion()
    motor.programar_evento(1, "POBLACION", imperio)
    motor.programar_evento(1, "ECONOMIA", imperio)
    motor.programar_evento(2, "ATAQUE", (imperio, rebeldes))  # Tupla (atacante, defensor)
    
    # 3. Ejecutamos y capturamos los logs
    logs_simulacion = motor.ejecutar_y_capturar_logs(fases=5) 
    
    # 4. Retornamos la respuesta a la vista de Tailwind
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "logs": logs_simulacion,
        "input_tesoro": tesoro_inicial,
        "input_tropas": tropas_imperio,
        "input_rebeldes": tropas_rebeldes
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

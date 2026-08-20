from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from engine import MotorSimulacion
from models import Faccion, Territorio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "logs": None, "metricas": None})

@app.post("/")
def ejecutar_simulacion(
    request: Request,
    tesoro_inicial: float = Form(200.0),
    tropas_imperio: int = Form(40),
    tropas_rebeldes: int = Form(25)
):
    motor = MotorSimulacion()
    
    # Configuración con los valores enviados desde tu formulario web
    imperio = Faccion(nombre="Imperio de Jade", tesoro_inicial=tesoro_inicial, costo_mantenimiento_unitario=15.0)
    imperio.ejercito = tropas_imperio
    imperio.moral = 80.0
    
    motor.facciones.append(imperio)
    
    rebeldes = Faccion(nombre="Rebeldes del Sur", tesoro_inicial=50.0, costo_mantenimiento_unitario=10.0)
    rebeldes.ejercito = tropas_rebeldes
    rebeldes.moral = 75.0
    
    capital = Territorio(nombre="Capital Primus", poblacion_inicial=1000, capacidad_carga=5000, tasa_impositiva=0.4)
    provincia = Territorio(nombre="Frontera Norte", poblacion_inicial=300, capacidad_carga=800, tasa_impositiva=0.2)
    imperio.agregar_territorio(capital)
    imperio.agregar_territorio(provincia)
    
    # Programar eventos
    motor.programar_evento(tiempo=1, tipo="POBLACION", referencia=imperio)
    motor.programar_evento(tiempo=1, tipo="ECONOMIA", referencia=imperio)
    motor.programar_evento(tiempo=2, tipo="ATAQUE", referencia=(imperio, rebeldes))
    
    # Ejecutamos usando el método que devuelve el diccionario con logs y métricas
    resultado = motor.ejecutar_y_capturar_logs(fases=5)
    
    print("--- DEBUG FASTAPI ---")
    print(f"Total Logs capturados: {len(resultado['logs'])}")
    print(f"Total Métricas capturadas: {len(resultado['metricas'])}")
    print("-----------------------")

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "logs": resultado["logs"],
        "metricas": resultado["metricas"],
        "input_tesoro": tesoro_inicial,
        "input_tropas": tropas_imperio,
        "input_rebeldes": tropas_rebeldes
    })
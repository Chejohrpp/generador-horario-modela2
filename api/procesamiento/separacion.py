import pandas as pd
from api.objetos.asignacion import Asignacion
from api.objetos.carrera import Carrera
from api.objetos.materia import Materia
from api.objetos.profesor import Profesor

from api.objetos.salon import Salon

def obtener_nombres_salones(path):
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(path)

    # Obtener los nombres de los salones como una lista
    nombres_salones = df['nombre_salon'].tolist()

    return nombres_salones

def obtener_clase_salones(path):
    salones = []  # Lista para almacenar instancias de la clase Salon

    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(path)

    # Iterar a través de las filas del DataFrame
    for index, row in df.iterrows():
        nombre_salon = row['nombre_salon']
        cantidad = row['cantidad']

        # Crear una instancia de la clase Salon y agregarla a la lista
        salon = Salon(nombre_salon, cantidad)
        salones.append(salon)

    return salones

def convertir_csv_a_profesores(path):
    profesores = []

    df = pd.read_csv(path)
    for index, row in df.iterrows():
        nombre_profesor = row['nombre_profesor']
        carreras = row['carrera']
        nuevo_profesor = Profesor(nombre_profesor, carreras)
        profesores.append(nuevo_profesor)

    return profesores

def convertir_csv_a_materias(path):
    materias = []

    try:
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            nombre_carrera = row['nombre_carrera']
            nombre_materia = row['nombre_materia']
            semestre = row['semestre']
            materia = Materia(nombre_carrera, nombre_materia, semestre)
            materias.append(materia)
            

    except FileNotFoundError:
        print(f"El archivo {path} no se encontró.")

    return materias

def convertir_csv_a_carreras(path):
    carreras = []
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        nombre_carrera = row['nombre_carrera']
        carrera = Carrera(nombre_carrera)
        carreras.append(carrera)
    return carreras

def convertir_csv_a_asignaciones(path):
    asignaciones = []
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        nombre_estudiante = row['nombre_estudiante']
        asignacion = Asignacion(nombre_estudiante)
        
        materias_seleccionadas = row['materias_seleccionadas']
        for materia in materias_seleccionadas.split(','):
            materia = materia.strip()
            asignacion.asignar_materia(materia)
            # asignacion.asignar_materia(Materia(materia))
        
        asignaciones.append(asignacion)
    return asignaciones

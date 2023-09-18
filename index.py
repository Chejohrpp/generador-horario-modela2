from api.carga_datos.HoraDia import array_hora_dia
from api.procesamiento.desicion import Scheduler
from api.procesamiento.separacion import convertir_csv_a_asignaciones, convertir_csv_a_carreras, convertir_csv_a_materias, convertir_csv_a_profesores, obtener_clase_salones, obtener_nombres_salones
from api.visualizacion.CreadorHorario import generar_imagen

from app import app  # Importa la instancia de la aplicación Flask desde app.py

# # Ruta de los archivos *en orden*
# path_salon = 'examples/salones.csv'
# path_profe = 'examples/profesor.csv'
# path_carrera = 'examples/carrera.csv'
# path_materia = 'examples/materia.csv'
# path_asignaciones = 'examples/asignacion.csv'

# # Llamar a la función para obtener los nombres de los salones
# array_salones = obtener_nombres_salones(path_salon)

# # ajustar la hora del dia
# hora_dia = array_hora_dia('15:20', 50, '22:00')
# # hora_dia = array_hora_dia('7:00', 30, '9:00')

# # Crear el arrays de objetos
# clases_salones = obtener_clase_salones(path_salon)
# profesores = convertir_csv_a_profesores(path_profe)
# carreras = convertir_csv_a_carreras(path_carrera)
# materias = convertir_csv_a_materias(path_materia)
# asignaciones = convertir_csv_a_asignaciones(path_asignaciones)

# # Generar el horario por la decision elegida (prioridad)
# scheduler = Scheduler()
# scheduler.cargar_datos_decision(clases_salones, profesores, carreras, materias, asignaciones, hora_dia)
# scheduler.seleccion_priridad()

# # lista del horario completo
# lista_horarios = scheduler.list_horarios()
# conflictos = scheduler.list_conflictos()
# eficiencia = scheduler.eficiencia_total()

# # for lista in lista_horarios:
# #     print(lista, "\n")

# # Mostrar imagen
# generar_imagen(array_salones,hora_dia,lista_horarios)


if __name__ == "__main__":
    app.run()  # Inicia la aplicación Flask
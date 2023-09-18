from flask_restful import Api, Resource, reqparse
from api.procesamiento.separacion import convertir_csv_a_asignaciones, convertir_csv_a_carreras, convertir_csv_a_materias, convertir_csv_a_profesores, obtener_clase_salones, obtener_nombres_salones
from api.visualizacion.CreadorHorario import generar_imagen
from api.carga_datos.HoraDia import array_hora_dia
from api.procesamiento.desicion import Scheduler

class ParametersApiHandler(Resource):
    # Ruta de los archivos *en orden*
    path_salon = 'examples/salones.csv'
    path_profe = 'examples/profesor.csv'
    path_carrera = 'examples/carrera.csv'
    path_materia = 'examples/materia.csv'
    path_asignaciones = 'examples/asignacion.csv'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hora_incio', type=str)
        parser.add_argument('hora_final', type=str)
        parser.add_argument('duracion', type=str)
        parser.add_argument('prioridad', type=str)
        
        args = parser.parse_args()

        print(args)

        # Empezar a procesar
        array_salones = obtener_nombres_salones(self.path_salon)

        # Extraer los datos
        request_hora_inicio = args['hora_incio']
        request_hora_final = args['hora_final']
        request_duracion = args['duracion']
        request_prioridad = args['prioridad']

        # consumir los datos
        ret_hora_inicio = request_hora_inicio
        ret_hora_final = request_hora_final
        ret_duracion = int(request_duracion)
        ret_prioridad = request_prioridad

        # ajustar la hora del dia
        hora_dia = array_hora_dia(ret_hora_inicio, ret_duracion, ret_hora_final)

        # Crear el arrays de objetos
        clases_salones = obtener_clase_salones(self.path_salon)
        profesores = convertir_csv_a_profesores(self.path_profe)
        carreras = convertir_csv_a_carreras(self.path_carrera)
        materias = convertir_csv_a_materias(self.path_materia)
        asignaciones = convertir_csv_a_asignaciones(self.path_asignaciones)

        # Generar el horario por la decision elegida (prioridad)
        scheduler = Scheduler()
        scheduler.cargar_datos_decision(clases_salones, profesores, carreras, materias, asignaciones, hora_dia)
        scheduler.seleccion_priridad(ret_prioridad)

        # lista del horario completo
        lista_horarios = scheduler.list_horarios()

        # datos a enviar al frontend
        conflictos = scheduler.list_conflictos()
        eficiencia = scheduler.eficiencia_total()

        # generar imagen
        generar_imagen(array_salones,hora_dia,lista_horarios)

        # enviar los datos al frontend
        respuesta = {
            "mensaje": "Horario generado con éxito",
            "conflictos": conflictos,
            "eficiencia": eficiencia
        }
        return respuesta


from api.objetos.horario import Horario
from api.objetos.asignacion import Asignacion
from api.objetos.carrera import Carrera
from api.objetos.materia import Materia
from api.objetos.profesor import Profesor

class Scheduler:
    def __init__(self):
        self.clases_salones = []
        self.profesores = []
        self.carreras = []
        self.materias = []
        self.asignaciones = []
        self.lista_horarios = []
        self.horas_definidas = []
        self.eficiencia = 1
        self.conflictos = []

    def list_horarios(self):
        return self.lista_horarios
    
    def list_conflictos(self):
        return self.conflictos

    # Prioridad predeterminada -> en base a la materia (semestre)
    def gen_horario_semestre(self):
        # Agrupar las materias por semestre
        materias_por_semestre = {}
        for materia in self.materias:
            semestre = materia.semestre
            if semestre not in materias_por_semestre:
                materias_por_semestre[semestre] = []
            materias_por_semestre[semestre].append(materia)

        # Ordenar las materias por semestre
        for semestre, materias in materias_por_semestre.items():
            materias_por_semestre[semestre] = sorted(materias, key=lambda x: x.semestre)

        # Inicializar una matriz de disponibilidad de horarios y salones
        disponibilidad = self.disponibilidad()

        # Generar horarios
        for semestre, materias in materias_por_semestre.items():
            for materia in materias:
                profesor_disponible = None
                horario_seleccionado = None
                salon_seleccionado = None
                conflicted = False

                # Buscar un horario y salón disponibles para la materia
                for salon in self.clases_salones:                         
                    prim_conflicto = {}
                    for horario in self.horas_definidas:
                        if disponibilidad[horario][salon]:                            
                            profesor_disponible = self.profesor_esta_disponible(horario, materia.carrera)
                            if profesor_disponible is not None:
                                # Check for semestre and carrera constraints
                                conflicted = False
                                for existing_horario in self.lista_horarios:
                                    if existing_horario.horario == horario and existing_horario.semestre == semestre and existing_horario.carrera == materia.carrera:
                                        if not prim_conflicto:
                                            prim_conflicto["profesor"] = profesor_disponible
                                            prim_conflicto["horario"] = horario
                                            prim_conflicto["salon"] = salon
                                        conflicted = True
                                        break
                                if not conflicted:
                                    horario_seleccionado = horario
                                    salon_seleccionado = salon
                                    break
                    if conflicted:
                        horario_seleccionado = prim_conflicto["horario"]
                        salon_seleccionado = prim_conflicto["salon"]
                        profesor_disponible = prim_conflicto["profesor"]
                        break
                    if salon_seleccionado:
                        break 
                                            

                if profesor_disponible and horario_seleccionado and salon_seleccionado:
                    # Crear un Horario y agregarlo a la lista
                    nuevo_horario = Horario(materia.nombre, horario_seleccionado, chr(65), profesor_disponible, salon_seleccionado.nombre, materia.carrera,semestre)
                    if conflicted : 
                        nuevo_horario.estilo('red')
                        # Generar aviso del conflicto
                        self.aviso_conflicto(f"La materia '{nuevo_horario.materia}' con seccion '{nuevo_horario.seccion}' tiene el mismo horario que un curso del mismo semestre")
                        

                    self.lista_horarios.append(nuevo_horario)

                    # Marcar el horario y salón como ocupados
                    disponibilidad[horario_seleccionado][salon_seleccionado] = False
                    
    def gent_horario_profesor(self):
        # Inicializar una matriz de disponibilidad de horarios y salones
        disponibilidad = self.disponibilidad()
        for materia in self.materias:
            profesor_disponible = None
            horario_seleccionado = None
            salon_seleccionado = None
            conflicted = False
            # Buscar un horario y salón disponibles para la materia
            for salon in self.clases_salones:
                print(salon)                                        
                prim_conflicto = {}
                for horario in self.horas_definidas:
                    if disponibilidad[horario][salon]:                            
                        profesor_disponible = self.profesor_esta_disponible(horario, materia.carrera)
                        if profesor_disponible is not None:
                            # Check for semestre and carrera constraints
                            conflicted = False
                            for existing_horario in self.lista_horarios:
                                if existing_horario.horario == horario and existing_horario.profesor == profesor_disponible:
                                    if not prim_conflicto:
                                        prim_conflicto["profesor"] = profesor_disponible
                                        prim_conflicto["horario"] = horario
                                        prim_conflicto["salon"] = salon
                                    conflicted = True
                                    break
                            if not conflicted:
                                horario_seleccionado = horario
                                salon_seleccionado = salon
                                break
                if conflicted:
                    horario_seleccionado = prim_conflicto["horario"]
                    salon_seleccionado = prim_conflicto["salon"]
                    profesor_disponible = prim_conflicto["profesor"]
                    break
                if salon_seleccionado:
                    break
            


    def disponibilidad(self):
        disponibilidad = {}
        for horario in self.horas_definidas:
            disponibilidad[horario] = {}
            for salon in self.clases_salones:
                disponibilidad[horario][salon] = True  # Inicialmente, todos los horarios y salones están disponibles
        return disponibilidad

    def profesor_esta_disponible(self, horario, materia_carrera):
        # Lógica para verificar la disponibilidad del profesor en el horario
        for profesor in self.profesores:
            if profesor.carrera == materia_carrera:
                conflicted = False
                for existing_horario in self.lista_horarios:
                    if existing_horario.horario == horario and existing_horario.carrera == materia_carrera and profesor.nombre == existing_horario.profesor:
                        conflicted = True
                        break
                if not conflicted : return profesor.nombre
        return None
    
    #Mensajes de los conflictos
    def aviso_conflicto(self, mensaje = None):
        #semestre
        #profesor
        #salon
        self.conflictos.append(mensaje)
    
    # Medidor de eficiencia
    def eficiencia_total(self):
        total_horarios = len(self.lista_horarios)
        total_conflicto = len(self.conflictos)
        perdida = total_conflicto / total_horarios
        self.eficiencia = self.eficiencia - perdida
        return self.eficiencia
    
    def generar_seccion(self, new_seccion):
        # partir en 2 la seccion
        
        # buscar un profesor 

        # si se puede usar el mismo horario en diferente salon

        # Crear seccion
        new_seccion += 1

    def verificar_salon_cantidad(self,salon, materia_nombre):
        # cuantos hay asignados
        cant_asignados = 0
        for asignados in self.asignaciones:
            for materia in asignados.materias_asignadas:
                if materia == materia_nombre:
                    cant_asignados += 1
        #  si el salon cabe o no
        if salon.cantidad_asientos < cant_asignados:
            return False
        return True            

    # seleccion que algoritmo usar
    def seleccion_priridad(self, opcion="materia"):
        if opcion.lower() == "materia":
            self.gen_horario_semestre()
        elif opcion.lower() == "profesor":
            print("self.gent_horario_profesor()")
        elif opcion.lower() == "salon":
            print("gen_horario_salon()")
        else:
            print("No prioridad encontrada")

    # En el archivo que tiene los arrays y la función cargar_datos
    def cargar_datos_decision(self, clases_salones, profesores, carreras, materias, asignaciones, horas_definidas):
        self.clases_salones = clases_salones
        self.profesores = profesores #carrera
        self.carreras = carreras
        self.materias = materias #carrera
        self.asignaciones = asignaciones #Tiene el curso
        self.horas_definidas = horas_definidas

        # Supongamos que tenemos una lista de carreras en minúsculas
        carreras_en_minusculas = [carrera.nombre.lower() for carrera in carreras]

        # Itera sobre las listas que tienen el atributo "carrera"
        for lista in [profesores, materias]:
            for elemento in lista:
                if elemento.carrera.lower() in carreras_en_minusculas:
                    # Convierte todos los elementos de la lista a mayúsculas
                    elemento.carrera = elemento.carrera.upper()
                else:
                    # Si la carrera no se encuentra en la lista, lanza una excepción
                    raise ValueError(f"La carrera '{elemento.carrera}' no está en la lista de carreras. revise el elemento '{elemento.nombre}'")


    def limpiar_datos(self):
        self.clases_salones = []
        self.profesores = []
        self.carreras = []
        self.materias = []
        self.asignaciones = []
        self.lista_horarios = []
        self.horas_definidas = []

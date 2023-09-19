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
        self.dif_eficiencia_total = 0

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
                if not (self.hay_disponibilidad(disponibilidad)):
                    self.aviso_conflicto(f"No hay espacio en el horario para la materia {materia.nombre} ")
                    continue
                profesor_disponible = None
                horario_seleccionado = None
                salon_seleccionado = None
                conflicted = False

                # Buscar un horario y salón disponibles para la materia
                for salon in self.clases_salones:
                    hay_espacio = self.verificar_salon_cantidad(salon,materia.nombre)
                    if not hay_espacio:
                        if salon == self.clases_salones[-1]:
                            #Agregar otra seccion o:
                            self.aviso_conflicto(f"No hay espacio en ningun salon para la materia {materia.nombre} ")
                            break
                        else:
                            continue
                    prim_conflicto = {}
                    for horario in self.horas_definidas:
                        if disponibilidad[horario][salon]:                            
                            profesor_disponible = self.profesor_esta_disponible(horario, materia.carrera)                            
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
                    elif salon == self.clases_salones[-1]:
                        self.aviso_conflicto(f"No hay salon disponibles para {materia.nombre}")
                        break

                if not profesor_disponible:
                    profesor_disponible = "NO PROFE"
                         

                if profesor_disponible and horario_seleccionado and salon_seleccionado:
                    # Crear un Horario y agregarlo a la lista
                    nuevo_horario = Horario(materia.nombre, horario_seleccionado, chr(65), profesor_disponible, salon_seleccionado.nombre, materia.carrera,semestre)
                    if conflicted :

                        # Mostrar precaucion
                        nuevo_horario.estilo('yellow')

                        # Generar aviso del conflicto
                        self.aviso_conflicto(f"La materia '{nuevo_horario.materia}' con seccion '{nuevo_horario.seccion}' tiene el mismo horario que un curso del mismo semestre")
                        
                    if profesor_disponible == "NO PROFE":
                        self.aviso_conflicto(f"No hay ningun profesor disponible para {nuevo_horario.materia} Seccion '{nuevo_horario.seccion}' ")
                        nuevo_horario.estilo('red')

                    self.lista_horarios.append(nuevo_horario)

                    # Marcar el horario y salón como ocupados
                    disponibilidad[horario_seleccionado][salon_seleccionado] = False

    # Prioridad 3, salones -> en base a la disponibilidad de espacios en los salones
    def gen_horario_salon(self):

        # Inicializar una matriz de disponibilidad de horarios y salones
        disponibilidad = self.disponibilidad()
        
        # Ordenar la lista de salones por cantidad de asientos, de menor a mayor
        salones_ordenados = sorted(self.clases_salones, key=lambda x: x.cantidad_asientos)

        # Ordenar la lista de materias por la cantidad de asignaciones, de menor a mayor
        materias_ordenadas = sorted(self.materias, key=lambda x: self.cant_asignados(x.nombre))

        # Selecciona materia
        for materia in materias_ordenadas:
            # Buscamos si aun hay horario disponibles
            if not (self.hay_disponibilidad(disponibilidad)):
                self.aviso_conflicto(f"No hay espacio en el horario para la materia {materia.nombre} ")
                continue

            # Variables necesarias
            profesor_disponible = None
            horario_seleccionado = None
            salon_seleccionado = None
            conflicted = False

            # Buscar un horario y salón disponibles para la materia, de la siguiente manera:
            for salon in salones_ordenados:
                hay_espacio = self.verificar_salon_cantidad(salon,materia.nombre)
                if hay_espacio:
                    for horario in self.horas_definidas:
                        if disponibilidad[horario][salon]:
                            profesor_disponible = self.profesor_esta_disponible(horario, materia.carrera)
                            horario_seleccionado = horario
                            salon_seleccionado = salon
                            break
                elif salon == self.clases_salones[-1]:
                        # buscar cualquier horario y salon disponible
                        salon_seleccionado, horario_seleccionado = self.get_salon_horario_vacio(disponibilidad)
                        if salon_seleccionado and horario_seleccionado:
                            conflicted = True
                        self.aviso_conflicto(f"No hay capacidad en ningun salon para '{materia.nombre}' ")
                        break
                if salon_seleccionado:
                    break
                        

            if not profesor_disponible:
                profesor_disponible = "NO PROFE"

            if horario_seleccionado and salon_seleccionado:
                # Crear un Horario y agregarlo a la lista
                nuevo_horario = Horario(materia.nombre, horario_seleccionado, chr(65), profesor_disponible, salon_seleccionado.nombre, materia.carrera,materia.semestre)

                if profesor_disponible == "NO PROFE":
                    self.aviso_conflicto(f"No hay ningun profesor disponible para {nuevo_horario.materia} Seccion '{nuevo_horario.seccion}' ")
                    nuevo_horario.estilo('yellow')

                if conflicted :
                    # Mostrar precaucion
                    nuevo_horario.estilo('red')

                    # Generar aviso del conflicto
                    self.aviso_conflicto(f"'{nuevo_horario.materia}' seccion '{nuevo_horario.seccion}' Esta en un salon que no tiene capacidad para las asignaciones")

                self.lista_horarios.append(nuevo_horario)

                # Marcar el horario y salón como ocupados
                disponibilidad[horario_seleccionado][salon_seleccionado] = False
            

    def disponibilidad(self):
        disponibilidad = {}
        for horario in self.horas_definidas:
            disponibilidad[horario] = {}
            for salon in self.clases_salones:
                disponibilidad[horario][salon] = True  # Inicialmente, todos los horarios y salones están disponibles
        return disponibilidad
    
    def hay_disponibilidad(self,disponibilidad):
        """
        Verifica si al menos hay un lugar en la matriz de disponibilidad.

        Args:
            disponibilidad: La matriz de disponibilidad.

        Returns:
            True si hay al menos un lugar, False en caso contrario.
        """
        return any(any(disponibilidad[horario][salon] for salon in disponibilidad[horario]) for horario in disponibilidad)

    def get_salon_horario_vacio(self,disponibilidad):
        for horario in self.horas_definidas:
            for salon in self.clases_salones:
                if disponibilidad[horario][salon]:
                    return salon, horario
        return None, None  # Si no se encuentra ningún horario y salón disponibles, retorna None, None


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
        self.dif_eficiencia_total += 1
        self.conflictos.append(mensaje)
    
    # Medidor de eficiencia
    def eficiencia_total(self):
        try:
            total_horarios = len(self.lista_horarios) + self.dif_eficiencia_total
            total_conflicto = len(self.conflictos)
            perdida = total_conflicto / total_horarios
            self.eficiencia = self.eficiencia - perdida
        except Exception as e:
            print(f"Ocurrió una excepción: {str(e)}")
            return 0
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

    def cant_asignados(self,materia_nombre):
        # cuantos hay asignados
        cant_asignados = 0
        for asignados in self.asignaciones:
            for materia in asignados.materias_asignadas:
                if materia == materia_nombre:
                    cant_asignados += 1
        print(materia_nombre,cant_asignados)
        return cant_asignados

    # seleccion que algoritmo usar
    def seleccion_priridad(self, opcion="materia"):
        if opcion.lower() == "materia":
            self.gen_horario_semestre()
        elif opcion.lower() == "profesor":
            print("self.gent_horario_profesor()")
        elif opcion.lower() == "salon":
            self.gen_horario_salon()
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

class Asignacion:
    def __init__(self, nombre_estudiante):
        self.nombre_estudiante = nombre_estudiante
        self.materias_asignadas = []

    def asignar_materia(self, materia):
        self.materias_asignadas.append(materia)

    def __str__(self):
        asignaciones = ", ".join([materia.nombre for materia in self.materias_asignadas])
        return f"Estudiante: {self.nombre_estudiante}, Materias Asignadas: {asignaciones}"

# # Ejemplo de uso
# estudiante1 = Asignacion("Juan Pérez")

# # Crear algunas materias
# materia1 = Materia("Programación 1", 2, carrera_sistemas)

# # Asignar materias a los estudiantes
# estudiante1.asignar_materia(materia1)

